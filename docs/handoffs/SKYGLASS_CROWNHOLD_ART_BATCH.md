# Art batch: Skyglass event and Crownhold (79 images)

- **Director, 2026-10-25:** "Draft up a design document for the art director to pull each prompt from and use references. Then a short compact hand off for each image in sequence and I hand you back the approved image."
- **Style (director, 2026-10-25):** every image in this batch is PREMIUM PIXEL ART, the same rendering as the Crownhold/crew avatars. Painted references (the Coffer, the charts, the jutsu exemplar) supply subject, materials and colours only; Arakane's avatar supplies the pixel rendering.
- **Protocol:** `docs/workflows/ISOLATED_ART_GENERATION.md`. One image per fresh session, at most two reference images (never a collage), one candidate at a time. The art director returns the RAW image; Claude Code keys, crops, exports and QCs it (`skills/producing-tnr-art`), then swaps the placeholder in game by manifest.
- **Pixel redraws (#36 to #46):** the event icons already live were painted; each is redrawn as pixel art from its own approved image so the whole set matches (director, 2026-10-25).
- **More pixel art (#47 onward):** the six Skyglass item icons inside the Coffer (redraws), then one scene per location the hunts actually depict (14; the wreck is now beached, and each Foundry room gets its own). Each scene lists the nodes that use it so the quests can be repointed when the art lands. Already pixel art and NOT redrawn: every crew avatar, the four scene portraits, the map structure. Left out: the retired Reliquary and old chests, and the retiring Ghost Ship quest icon.
- **Not in this batch:** Arakane (done, `art/crownhold/avatar_crownhold_arakane.webp`); the Sealwright and Oathkeeper scene portraits (already exist). **Deferred:** the Lastlight hit animation (a vertical strip sprite sheet; its placeholder is KGK: Black Fang Lance's).
- **How a session uses this file:** it is given the link to this file and an image number. It reads that image's section, downloads the reference images from the links there, attaches them in the order given, and runs the prompt exactly as written.
- **Live-game requests/writes:** 0.

## Session contract (every image, no exceptions)

1. **The operator attaches the reference files from that image's folder** in `skyglass_art_batch.zip` (one folder per image: `ref1_*`, `ref2_*` in attach order, plus `prompt.txt`). Art sessions have no network access. The raw URLs below are the canonical source. Never use a text-only repository connector: it cannot return images.
2. **Verify each attached file:** it is present and shows the described subject. Width x height, byte size and SHA-256 describe the original and are informational only: chat uploads are resized and recompressed.
3. **Show each reference back** (display it) and confirm it is attached to the generation request, in the listed order, with its listed role.
4. **Abort if any reference is missing, fails verification or cannot be attached.** Report which one and stop. Never generate without all references.
5. **Copy the fenced prompt (or the folder's `prompt.txt`) verbatim.** Do not shorten, summarise or rewrite it.
6. Generate exactly one candidate. Do not crop, key, resize or otherwise process it. Return the raw image under the name the prompt gives.

## Targets (from `25x_DATA_art_spec.json`)

| Target | Canvas to generate | Key | Delivered |
|---|---|---|---|
| ICON | 1024 x 1024 | lime (magenta when the subject is green or the brief says so) | 256 px webp |
| JUTSU_ICON | 1024 x 1024 | none: designed background allowed (RUL-2026-10-14-001) | 256 px webp |
| AI_AVATAR | 1024 x 1024 | magenta | square webp, up to 1024 px |
| SCENE_BACKGROUND | 1536 x 1024 (3:2) | none | 512 x 341 webp |

## Reference files

Every link is pinned to commit `60b792ac19ba710d724a247127eb0482d967eeaf`, so it never changes. A fresh session downloads the images named in its section and attaches them.

| Key | Image link | Bytes | W x H | SHA-256 |
|---|---|---|---|---|
| coffer | https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/skyglass_event_icons/exports/icon-skyglass-coffer.webp | 70574 | 256 x 256 | `a7bbfe7e60570aef4e25d2c4492d4eb31d32318b800164545c71883f7e0113d3` |
| foundry_chart | https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/skyglass_event_icons/exports/icon-chart-drowned-foundry.webp | 60940 | 256 x 256 | `0b00806939bd375a74086f095956a2b0f924d87e12aedb83cfa1d1ee9058182b` |
| lantern | https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/skyglass_event_icons/exports/icon-skyglass-signal-beacon.webp | 45678 | 256 x 256 | `6b58863e0d526502ab16dc462d09ecbb434b0f68ed699b7a7004dcc71d226ff1` |
| crown | https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/icon_ghost_ship_skyglass_crown.webp | 116290 | 480 x 480 | `02cde28f5fedfaf370fc1988fd13457d370731bdbe1572e0f3638d767f68a876` |
| arakane | https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/crownhold/avatar_crownhold_arakane.webp | 289646 | 1239 x 1239 | `0383691812dc34673b01fd71023a6191b36fbcbab55634d18cf11d62947436b8` |
| arsenal | https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_arsenal_keeper.webp | 191438 | 1241 x 1241 | `1caf87b04c7ecd4cd2d3dd4569a93036d61fbef858acd0dc16c4a92370ac2858` |
| deck_warden | https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_deck_warden.webp | 123206 | 1221 x 1221 | `805c1e99bcb1e7b337b20374add6a581228871da2d6b90a89ce57e154b91bdd0` |
| captain | https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_captain_b.webp | 203140 | 1235 x 1235 | `ce93b9dc6cd70e79aa2454662ad1e1881d78c4e0fb260fdfda7898017510ff6b` |
| seal_charge | https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_seal_charge.webp | 153182 | 1174 x 1174 | `6f56d9c84465f970e1204cd75f9d478d71d37abc3d66430febad8f548f8bd01b` |
| bbe | https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/style_refs/jutsu_icons/bbe/icon_bbe_sapphire_command_v2.webp | 61270 | 256 x 256 | `410b8c5a20af40b27aaf728d5d8c7b2260adc500c7dd64187b08c0953e6531c5` |
| gallery | https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp | 250006 | 1536 x 1024 | `babd22ccf728fb67c8208f1f68af8c5eb3286c3a76bdcbe0e1b2b0bdf227026c` |
| helm | https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_helm.webp | 329520 | 1536 x 1024 | `d72d0506b07b59a917017371ff2c1b4c7d84532d0625d661523109de78eef9ce` |
| captain_portrait | https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp | 85260 | 728 x 728 | `60087ce9e1d640199a7a61aceb154fc783beb1408fa89de5d869dfe7854462a5` |
| treasury_subject | https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/skyglass_event_icons/raw/subject_sealed_treasury_painted_v1.webp | 260686 | 1254 x 1254 | `ba32444763970bb65ab81a0fbca4821384b2ebd92a5d94e43f07faad52921ad2` |
| redraw_icon-tool-pouch-katon.webp | https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/skyglass_event_icons/exports/icon-tool-pouch-katon.webp | 67920 | 256 x 256 | `b1fa26ced2204d1e3206dbdf418b34f5949bffc2054d0d7cfcc2404334808d6b` |
| redraw_icon-tool-pouch-wave.webp | https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/skyglass_event_icons/exports/icon-tool-pouch-wave.webp | 67620 | 256 x 256 | `44fa5437a835a3e004d4788127518af760718445f3e3b1ef8888600cd7eeeba8` |
| redraw_icon-tool-pouch-ikazuchi.webp | https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/skyglass_event_icons/exports/icon-tool-pouch-ikazuchi.webp | 68698 | 256 x 256 | `c644532a96cbf44eba6c1e4d082c08144ee51a577143ba357c2b93add10fc515` |
| redraw_icon-tool-pouch-stonefall.webp | https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/skyglass_event_icons/exports/icon-tool-pouch-stonefall.webp | 68232 | 256 x 256 | `029a560a5bcbc202da9e41421e251cf73fca938dc7cfa21593b9fe43aecba07c` |
| redraw_icon-tool-pouch-zephyrfang.webp | https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/skyglass_event_icons/exports/icon-tool-pouch-zephyrfang.webp | 66358 | 256 x 256 | `ca3d144715e8385bc0db61c65fdc62a01afea7db0cc7470017ea0daa591a4d4d` |
| redraw_icon-chart-quarantined-archive.webp | https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/skyglass_event_icons/exports/icon-chart-quarantined-archive.webp | 65754 | 256 x 256 | `80df641bad0135e78b52bc508440dbe9c160d477d50d98f16ccef3da23dc2432` |
| redraw_icon-chart-captains-watch.webp | https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/skyglass_event_icons/exports/icon-chart-captains-watch.webp | 68722 | 256 x 256 | `e576a50a3f066e972fc09974592a83d8cf6cae5c18e10200776bd503d3f77b8e` |
| redraw_icon-armory-requisition.webp | https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/skyglass_event_icons/exports/icon-armory-requisition.webp | 47944 | 256 x 256 | `869b66de517273adfa5432d08d1cd2d0a95db825ac47b6e527ceb702cfc96c83` |
| redraw_icon_ghost_ship_skyglass_crown_fragment.webp | https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/icon_ghost_ship_skyglass_crown_fragment.webp | 107374 | 480 x 480 | `434872cd478550ca3ec2791e382c8c444c5e020664ea3c6057dcc9089be07e30` |
| redraw_icon_ghost_ship_skyglass_crystal.webp | https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/icon_ghost_ship_skyglass_crystal.webp | 103342 | 480 x 480 | `896543c69115e830b1016b966fbfbcdab3ebf676d10e05ac24cb3b9e7d604dfc` |
| redraw_icon_ghost_ship_skyglass_filament.webp | https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/icon_ghost_ship_skyglass_filament.webp | 129168 | 480 x 480 | `b165dba7e5849bcd25ca40bb90532b7787bc125973589b52864669e69ee6328d` |
| redraw_icon_ghost_ship_skyglass_katana.webp | https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/icon_ghost_ship_skyglass_katana.webp | 56510 | 480 x 480 | `f7a336ca9fc0067a57ec2a69a0d3120a8790531ad83c5236306cdd8be92af8cc` |
| redraw_icon_ghost_ship_skyglass_serum.webp | https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/icon_ghost_ship_skyglass_serum.webp | 277032 | 768 x 768 | `6d83e870aa4bdbd8c918256c5dc3e9c4f338ed59aa11a1ec033b8e5e27a343c5` |
| scene_exterior_keel_walk | https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_exterior_keel_walk.webp | 224364 | 1536 x 1024 | `f665ca4bb8bc4da031241d4b7275359409e6a6a7a711dce0874bd1d1cebfd70a` |
| scene_lower_hull | https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_lower_hull.webp | 443164 | 1536 x 1024 | `5906fa63576bb8789078f3c2e0adad09da543963cce94a42956f795c682dcd07` |
| scene_hold | https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_hold.webp | 311832 | 1536 x 1024 | `6743482693564c430c8e95426ea6595af0a2b20ad1768b10140f7d8a95da2fd5` |
| scene_reconstruction_chamber | https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_reconstruction_chamber.webp | 446336 | 1470 x 980 | `d0b0c3297409638c2c02b6314dbd817d7c71875e455d70a966238471d6d4552e` |
| scene_quarantined_archive | https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_quarantined_archive.webp | 344950 | 1536 x 1024 | `25682147baa0fd69bf8790db174eb64665c11bd51c2a42400b945c9ba66c3f8f` |
| scene_cache_site | https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_cache_site.webp | 156820 | 1536 x 1024 | `4ad71d71d9794353d28faf0f691a9772f7e6c0ea10df71927751a49bf11e7ead` |
| scene_chart_room | https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_chart_room.webp | 378286 | 1536 x 1024 | `ed6ae32d26e8b586ef3749f1d3e45dea86af84c4a05e4576351457f627b0f426` |
| scene_deck_b | https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_deck_b.webp | 355890 | 1536 x 1024 | `e6004e0ab8749afc2c40776ee7fc6b3b4532226997068f0bdccae6078971dad0` |

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
| 8 | Master of Arms (commander) | AI_AVATAR | magenta | seal_charge | `avatar_crownhold_master_of_arms.webp` |
| 9 | Replicant Zero (commander) | AI_AVATAR | magenta | seal_charge | `avatar_crownhold_replicant_zero.webp` |
| 10 | The Grand Marshal (commander) | AI_AVATAR | magenta | seal_charge | `avatar_crownhold_the_grand_marshal.webp` |
| 11 | Crownhold Proving Proctor | AI_AVATAR | magenta | seal_charge | `avatar_crownhold_proving_proctor.webp` |
| 12 | Ordnance Quartermaster | AI_AVATAR | magenta | seal_charge | `avatar_crownhold_ordnance_quartermaster.webp` |
| 13 | Prototype Lancer Unit | AI_AVATAR | magenta | seal_charge | `avatar_crownhold_prototype_lancer_unit.webp` |
| 14 | Calibration Duelist | AI_AVATAR | magenta | seal_charge | `avatar_crownhold_calibration_duelist.webp` |
| 15 | Skyglass Archive Keeper | AI_AVATAR | magenta | seal_charge | `avatar_crownhold_skyglass_archive_keeper.webp` |
| 16 | Impression Containment Warden | AI_AVATAR | magenta | seal_charge | `avatar_crownhold_impression_containment_warden.webp` |
| 17 | Unstable Echo Subject | AI_AVATAR | magenta | seal_charge | `avatar_crownhold_unstable_echo_subject.webp` |
| 18 | Failed Reconstruction Prototype | AI_AVATAR | magenta | seal_charge | `avatar_crownhold_failed_reconstruction_prototype.webp` |
| 19 | Command Signal Adjutant | AI_AVATAR | magenta | seal_charge | `avatar_crownhold_command_signal_adjutant.webp` |
| 20 | High Command Staff Tactician | AI_AVATAR | magenta | seal_charge | `avatar_crownhold_high_command_staff_tactician.webp` |
| 21 | Honor Guard Commandant | AI_AVATAR | magenta | seal_charge | `avatar_crownhold_honor_guard_commandant.webp` |
| 22 | Strategist's Aide-de-Camp | AI_AVATAR | magenta | seal_charge | `avatar_crownhold_strategists_aide_de_camp.webp` |
| 23 | Sanctum Vanguard | AI_AVATAR | magenta | seal_charge | `avatar_crownhold_sanctum_vanguard.webp` |
| 24 | Directive Herald | AI_AVATAR | magenta | seal_charge | `avatar_crownhold_directive_herald.webp` |
| 25 | Last Watch Executor | AI_AVATAR | magenta | seal_charge | `avatar_crownhold_last_watch_executor.webp` |
| 26 | Order-Bearer of the Sanctum | AI_AVATAR | magenta | seal_charge | `avatar_crownhold_order_bearer_of_the_sanctum.webp` |
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

1. SUBJECT: redraw this exact chest: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/skyglass_event_icons/raw/subject_sealed_treasury_painted_v1.webp  (260686 bytes, 1254 x 1254, sha256 `ba32444763970bb6…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/crownhold/avatar_crownhold_arakane.webp  (289646 bytes, 1239 x 1239, sha256 `0383691812dc3467…`)

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

1. CHART FAMILY: shape and materials (painted: redraw as pixel art): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/skyglass_event_icons/exports/icon-chart-drowned-foundry.webp  (60940 bytes, 256 x 256, sha256 `0b00806939bd375a…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/crownhold/avatar_crownhold_arakane.webp  (289646 bytes, 1239 x 1239, sha256 `0383691812dc3467…`)

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

1. SHAPE AND LAYOUT (painted: redraw as pixel art): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/skyglass_event_icons/exports/icon-chart-drowned-foundry.webp  (60940 bytes, 256 x 256, sha256 `0b00806939bd375a…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/crownhold/avatar_crownhold_arakane.webp  (289646 bytes, 1239 x 1239, sha256 `0383691812dc3467…`)

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

1. MATERIAL AND COLOURS (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/skyglass_event_icons/exports/icon-skyglass-coffer.webp  (70574 bytes, 256 x 256, sha256 `a7bbfe7e60570aef…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/crownhold/avatar_crownhold_arakane.webp  (289646 bytes, 1239 x 1239, sha256 `0383691812dc3467…`)

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

1. SUBJECT: keep the crown exactly: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/crownhold/avatar_crownhold_arakane.webp  (289646 bytes, 1239 x 1239, sha256 `0383691812dc3467…`)
2. STYLE: icon rendering only: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/icon_ghost_ship_skyglass_crown.webp  (116290 bytes, 480 x 480, sha256 `02cde28f5fedfaf3…`)

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

1. STYLE: jutsu icon register: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/style_refs/jutsu_icons/bbe/icon_bbe_sapphire_command_v2.webp  (61270 bytes, 256 x 256, sha256 `410b8c5a20af40b2…`)
2. MOTIF: the lantern's light: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/skyglass_event_icons/exports/icon-skyglass-signal-beacon.webp  (45678 bytes, 256 x 256, sha256 `6b58863e0d526502…`)

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

1. STYLE: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_arsenal_keeper.webp  (191438 bytes, 1241 x 1241, sha256 `1caf87b04c7ecd4c…`)

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

1. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (it is an object, not a character; the figure is described entirely by the text): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_seal_charge.webp  (153182 bytes, 1174 x 1174, sha256 `6f56d9c84465f970…`)

~~~text
Draw ONE image for The Ninja RPG: Master of Arms (commander). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (it is an object, not a character; the figure is described entirely by the text). Follow each reference only for its stated role.

Subject: Master of Arms: Division I commander. A broad, bull-necked weapons master: a dented iron half-helm with a forge-orange lacquered face guard over the mouth and jaw, a bald or close-cropped head (no long hair, no topknot); heavy lacquered plates over dark indigo cloth, a war-axe and a heavy cleaver-blade in his hands, more blades and a spear slung across his back; calm and exacting. Accent: forge-orange. Commander presence: clearly a commander, not a rank-and-file officer: larger and heavier-built, a heavier layered coat or cloak with a high collar, more fittings and wraps, a commanding stance. No crown, no gold.

Continuity (Crownhold): a shinobi of the Skyglass Project's mountain fortress, recalled as a chakra impression. Dress him in the same outfit language as the style reference's crew: practical ninja gear (dark indigo and stone-grey cloth, rope and leather wraps, plain lacquered plates and bracers, a cloth mask or headwrap over the face), worn and weathered, solid and grounded. The only sign he is an impression: eyes lit with pale chakra and a faint chakra haze at the cloth's ragged edges. No glowing seams or veins, no translucent or crystal body, no gold filigree, no tassels, no crown, no technology. Closed boots or wrapped tabi footwear, no bare toes. No thread, wire or line rising from the head or neck. Palette: mountain-stone greys, dark indigo cloth, dull brass fittings, plus the one accent named in the subject.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_master_of_arms.png.
~~~

### 9. Replicant Zero (commander)

References (download and attach, in this order):

1. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (it is an object, not a character; the figure is described entirely by the text): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_seal_charge.webp  (153182 bytes, 1174 x 1174, sha256 `6f56d9c84465f970…`)

~~~text
Draw ONE image for The Ninja RPG: Replicant Zero (commander). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (it is an object, not a character; the figure is described entirely by the text). Follow each reference only for its stated role.

Subject: Replicant Zero: Division II commander. A tall, composed medical-nin: a plain dark grey hood and a dark cloth face mask, both eyes lit pale violet; a long layered dark field coat with a high stiff collar, a medic's scroll case and a row of sealing-tag pouches across the chest; his left hand and forearm sheathed in a steady glow of pale violet healing chakra as he works on them (the hand whole and solid, glowing like a medic's hands mid-treatment); the first successful recall; calm and curious. No sword. Accent: pale violet. Commander presence: clearly a commander, not a rank-and-file officer: larger and heavier-built, a heavier layered coat or cloak with a high collar, more fittings and wraps, a commanding stance. No crown, no gold.

Continuity (Crownhold): a shinobi of the Skyglass Project's mountain fortress, recalled as a chakra impression. Dress him in the same outfit language as the style reference's crew: practical ninja gear (dark indigo and stone-grey cloth, rope and leather wraps, plain lacquered plates and bracers, a cloth mask or headwrap over the face), worn and weathered, solid and grounded. The only sign he is an impression: eyes lit with pale chakra and a faint chakra haze at the cloth's ragged edges. No glowing seams or veins, no translucent or crystal body, no gold filigree, no tassels, no crown, no technology. Closed boots or wrapped tabi footwear, no bare toes. No thread, wire or line rising from the head or neck. Palette: mountain-stone greys, dark indigo cloth, dull brass fittings, plus the one accent named in the subject.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_replicant_zero.png.
~~~

### 10. The Grand Marshal (commander)

References (download and attach, in this order):

1. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (it is an object, not a character; the figure is described entirely by the text): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_seal_charge.webp  (153182 bytes, 1174 x 1174, sha256 `6f56d9c84465f970…`)

~~~text
Draw ONE image for The Ninja RPG: The Grand Marshal (commander). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (it is an object, not a character; the figure is described entirely by the text). Follow each reference only for its stated role.

Subject: The Grand Marshal: Division III commander, called 'The Second'. An older senior shinobi officer: a wide flat travelling hat with a muted-brass brim band shading a plain dark cloth mask, a short grey beard visible below it; a plain dark long coat over light plates, hands clasped behind his back, no drawn weapon; thoughtful and severe; the deputy who could question orders. Accent: muted brass. Commander presence: clearly a commander, not a rank-and-file officer: larger and heavier-built, a heavier layered coat or cloak with a high collar, more fittings and wraps, a commanding stance. No crown, no gold.

Continuity (Crownhold): a shinobi of the Skyglass Project's mountain fortress, recalled as a chakra impression. Dress him in the same outfit language as the style reference's crew: practical ninja gear (dark indigo and stone-grey cloth, rope and leather wraps, plain lacquered plates and bracers, a cloth mask or headwrap over the face), worn and weathered, solid and grounded. The only sign he is an impression: eyes lit with pale chakra and a faint chakra haze at the cloth's ragged edges. No glowing seams or veins, no translucent or crystal body, no gold filigree, no tassels, no crown, no technology. Closed boots or wrapped tabi footwear, no bare toes. No thread, wire or line rising from the head or neck. Palette: mountain-stone greys, dark indigo cloth, dull brass fittings, plus the one accent named in the subject.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_the_grand_marshal.png.
~~~

### 11. Crownhold Proving Proctor

References (download and attach, in this order):

1. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (it is an object, not a character; the figure is described entirely by the text): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_seal_charge.webp  (153182 bytes, 1174 x 1174, sha256 `6f56d9c84465f970…`)

~~~text
Draw ONE image for The Ninja RPG: Crownhold Proving Proctor. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (it is an object, not a character; the figure is described entirely by the text). Follow each reference only for its stated role.

Subject: Crownhold Proving Proctor: Division I. An armory proctor in a faded grey drill wrap and cloth headwrap, a wooden board of trial slips in one hand, two wooden practice blades at the hip, a whistle on a cord. Accent: drill-yellow.

Continuity (Crownhold): a shinobi of the Skyglass Project's mountain fortress, recalled as a chakra impression. Dress him in the same outfit language as the style reference's crew: practical ninja gear (dark indigo and stone-grey cloth, rope and leather wraps, plain lacquered plates and bracers, a cloth mask or headwrap over the face), worn and weathered, solid and grounded. The only sign he is an impression: eyes lit with pale chakra and a faint chakra haze at the cloth's ragged edges. No glowing seams or veins, no translucent or crystal body, no gold filigree, no tassels, no crown, no technology. Closed boots or wrapped tabi footwear, no bare toes. No thread, wire or line rising from the head or neck. Palette: mountain-stone greys, dark indigo cloth, dull brass fittings, plus the one accent named in the subject.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_proving_proctor.png.
~~~

### 12. Ordnance Quartermaster

References (download and attach, in this order):

1. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (it is an object, not a character; the figure is described entirely by the text): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_seal_charge.webp  (153182 bytes, 1174 x 1174, sha256 `6f56d9c84465f970…`)

~~~text
Draw ONE image for The Ninja RPG: Ordnance Quartermaster. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (it is an object, not a character; the figure is described entirely by the text). Follow each reference only for its stated role.

Subject: Ordnance Quartermaster: Division I. A soot-stained apron over a field vest, bandoliers of glowing explosive tags, soot-dark gloves holding a tray of tags. Accent: tag-orange.

Continuity (Crownhold): a shinobi of the Skyglass Project's mountain fortress, recalled as a chakra impression. Dress him in the same outfit language as the style reference's crew: practical ninja gear (dark indigo and stone-grey cloth, rope and leather wraps, plain lacquered plates and bracers, a cloth mask or headwrap over the face), worn and weathered, solid and grounded. The only sign he is an impression: eyes lit with pale chakra and a faint chakra haze at the cloth's ragged edges. No glowing seams or veins, no translucent or crystal body, no gold filigree, no tassels, no crown, no technology. Closed boots or wrapped tabi footwear, no bare toes. No thread, wire or line rising from the head or neck. Palette: mountain-stone greys, dark indigo cloth, dull brass fittings, plus the one accent named in the subject.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_ordnance_quartermaster.png.
~~~

### 13. Prototype Lancer Unit

References (download and attach, in this order):

1. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (it is an object, not a character; the figure is described entirely by the text): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_seal_charge.webp  (153182 bytes, 1174 x 1174, sha256 `6f56d9c84465f970…`)

~~~text
Draw ONE image for The Ninja RPG: Prototype Lancer Unit. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (it is an object, not a character; the figure is described entirely by the text). Follow each reference only for its stated role.

Subject: Prototype Lancer Unit: Division I. A spear specialist in light plates, a long cross-bladed spear crackling with lightning chakra, chakra-burn scars wrapped on both forearms. Accent: electric yellow.

Continuity (Crownhold): a shinobi of the Skyglass Project's mountain fortress, recalled as a chakra impression. Dress him in the same outfit language as the style reference's crew: practical ninja gear (dark indigo and stone-grey cloth, rope and leather wraps, plain lacquered plates and bracers, a cloth mask or headwrap over the face), worn and weathered, solid and grounded. The only sign he is an impression: eyes lit with pale chakra and a faint chakra haze at the cloth's ragged edges. No glowing seams or veins, no translucent or crystal body, no gold filigree, no tassels, no crown, no technology. Closed boots or wrapped tabi footwear, no bare toes. No thread, wire or line rising from the head or neck. Palette: mountain-stone greys, dark indigo cloth, dull brass fittings, plus the one accent named in the subject.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_prototype_lancer_unit.png.
~~~

### 14. Calibration Duelist

References (download and attach, in this order):

1. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (it is an object, not a character; the figure is described entirely by the text): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_seal_charge.webp  (153182 bytes, 1174 x 1174, sha256 `6f56d9c84465f970…`)

~~~text
Draw ONE image for The Ninja RPG: Calibration Duelist. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (it is an object, not a character; the figure is described entirely by the text). Follow each reference only for its stated role.

Subject: Calibration Duelist: Division I. A young duelist in sparring wraps, a practice sword wrapped in wind chakra, an apprentice cord on the shoulder. Accent: wind-green.

Continuity (Crownhold): a shinobi of the Skyglass Project's mountain fortress, recalled as a chakra impression. Dress him in the same outfit language as the style reference's crew: practical ninja gear (dark indigo and stone-grey cloth, rope and leather wraps, plain lacquered plates and bracers, a cloth mask or headwrap over the face), worn and weathered, solid and grounded. The only sign he is an impression: eyes lit with pale chakra and a faint chakra haze at the cloth's ragged edges. No glowing seams or veins, no translucent or crystal body, no gold filigree, no tassels, no crown, no technology. Closed boots or wrapped tabi footwear, no bare toes. No thread, wire or line rising from the head or neck. Palette: mountain-stone greys, dark indigo cloth, dull brass fittings, plus the one accent named in the subject.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_calibration_duelist.png.
~~~

### 15. Skyglass Archive Keeper

References (download and attach, in this order):

1. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (it is an object, not a character; the figure is described entirely by the text): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_seal_charge.webp  (153182 bytes, 1174 x 1174, sha256 `6f56d9c84465f970…`)

~~~text
Draw ONE image for The Ninja RPG: Skyglass Archive Keeper. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (it is an object, not a character; the figure is described entirely by the text). Follow each reference only for its stated role.

Subject: Skyglass Archive Keeper: Division II. An archivist-nin with a satchel of scrolls and a bound ledger, ink-stained fingers, a small skyglass reading lens on a cord. Accent: archive blue.

Continuity (Crownhold): a shinobi of the Skyglass Project's mountain fortress, recalled as a chakra impression. Dress him in the same outfit language as the style reference's crew: practical ninja gear (dark indigo and stone-grey cloth, rope and leather wraps, plain lacquered plates and bracers, a cloth mask or headwrap over the face), worn and weathered, solid and grounded. The only sign he is an impression: eyes lit with pale chakra and a faint chakra haze at the cloth's ragged edges. No glowing seams or veins, no translucent or crystal body, no gold filigree, no tassels, no crown, no technology. Closed boots or wrapped tabi footwear, no bare toes. No thread, wire or line rising from the head or neck. Palette: mountain-stone greys, dark indigo cloth, dull brass fittings, plus the one accent named in the subject.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_skyglass_archive_keeper.png.
~~~

### 16. Impression Containment Warden

References (download and attach, in this order):

1. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (it is an object, not a character; the figure is described entirely by the text): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_seal_charge.webp  (153182 bytes, 1174 x 1174, sha256 `6f56d9c84465f970…`)

~~~text
Draw ONE image for The Ninja RPG: Impression Containment Warden. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (it is an object, not a character; the figure is described entirely by the text). Follow each reference only for its stated role.

Subject: Impression Containment Warden: Division II. A sealing specialist in a hooded wrap, a heavy ring of seal keys and tag-wrapped scroll cases on chains, a water-filled seal jar at the hip. Accent: water teal.

Continuity (Crownhold): a shinobi of the Skyglass Project's mountain fortress, recalled as a chakra impression. Dress him in the same outfit language as the style reference's crew: practical ninja gear (dark indigo and stone-grey cloth, rope and leather wraps, plain lacquered plates and bracers, a cloth mask or headwrap over the face), worn and weathered, solid and grounded. The only sign he is an impression: eyes lit with pale chakra and a faint chakra haze at the cloth's ragged edges. No glowing seams or veins, no translucent or crystal body, no gold filigree, no tassels, no crown, no technology. Closed boots or wrapped tabi footwear, no bare toes. No thread, wire or line rising from the head or neck. Palette: mountain-stone greys, dark indigo cloth, dull brass fittings, plus the one accent named in the subject.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_impression_containment_warden.png.
~~~

### 17. Unstable Echo Subject

References (download and attach, in this order):

1. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (it is an object, not a character; the figure is described entirely by the text): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_seal_charge.webp  (153182 bytes, 1174 x 1174, sha256 `6f56d9c84465f970…`)

~~~text
Draw ONE image for The Ninja RPG: Unstable Echo Subject. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (it is an object, not a character; the figure is described entirely by the text). Follow each reference only for its stated role.

Subject: Unstable Echo Subject: Division II. A ninja caught mid-step splitting into an imperfect shadow clone: the clone a half-step behind and out of line, shadow chakra trailing between them. Accent: shadow violet.

Continuity (Crownhold): a shinobi of the Skyglass Project's mountain fortress, recalled as a chakra impression. Dress him in the same outfit language as the style reference's crew: practical ninja gear (dark indigo and stone-grey cloth, rope and leather wraps, plain lacquered plates and bracers, a cloth mask or headwrap over the face), worn and weathered, solid and grounded. The only sign he is an impression: eyes lit with pale chakra and a faint chakra haze at the cloth's ragged edges. No glowing seams or veins, no translucent or crystal body, no gold filigree, no tassels, no crown, no technology. Closed boots or wrapped tabi footwear, no bare toes. No thread, wire or line rising from the head or neck. Palette: mountain-stone greys, dark indigo cloth, dull brass fittings, plus the one accent named in the subject.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_unstable_echo_subject.png.
~~~

### 18. Failed Reconstruction Prototype

References (download and attach, in this order):

1. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (it is an object, not a character; the figure is described entirely by the text): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_seal_charge.webp  (153182 bytes, 1174 x 1174, sha256 `6f56d9c84465f970…`)

~~~text
Draw ONE image for The Ninja RPG: Failed Reconstruction Prototype. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (it is an object, not a character; the figure is described entirely by the text). Follow each reference only for its stated role.

Subject: Failed Reconstruction Prototype: Division II. A hulking earth-style ninja half-encased in his own stone armour technique, rock plating cracked over one arm and shoulder, rope-bound. Accent: stone ochre.

Continuity (Crownhold): a shinobi of the Skyglass Project's mountain fortress, recalled as a chakra impression. Dress him in the same outfit language as the style reference's crew: practical ninja gear (dark indigo and stone-grey cloth, rope and leather wraps, plain lacquered plates and bracers, a cloth mask or headwrap over the face), worn and weathered, solid and grounded. The only sign he is an impression: eyes lit with pale chakra and a faint chakra haze at the cloth's ragged edges. No glowing seams or veins, no translucent or crystal body, no gold filigree, no tassels, no crown, no technology. Closed boots or wrapped tabi footwear, no bare toes. No thread, wire or line rising from the head or neck. Palette: mountain-stone greys, dark indigo cloth, dull brass fittings, plus the one accent named in the subject.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_failed_reconstruction_prototype.png.
~~~

### 19. Command Signal Adjutant

References (download and attach, in this order):

1. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (it is an object, not a character; the figure is described entirely by the text): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_seal_charge.webp  (153182 bytes, 1174 x 1174, sha256 `6f56d9c84465f970…`)

~~~text
Draw ONE image for The Ninja RPG: Command Signal Adjutant. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (it is an object, not a character; the figure is described entirely by the text). Follow each reference only for its stated role.

Subject: Command Signal Adjutant: Division III. A signals ninja with a semaphore flag in each hand, a message-scroll tube across the back, a rank cord. Accent: signal green.

Continuity (Crownhold): a shinobi of the Skyglass Project's mountain fortress, recalled as a chakra impression. Dress him in the same outfit language as the style reference's crew: practical ninja gear (dark indigo and stone-grey cloth, rope and leather wraps, plain lacquered plates and bracers, a cloth mask or headwrap over the face), worn and weathered, solid and grounded. The only sign he is an impression: eyes lit with pale chakra and a faint chakra haze at the cloth's ragged edges. No glowing seams or veins, no translucent or crystal body, no gold filigree, no tassels, no crown, no technology. Closed boots or wrapped tabi footwear, no bare toes. No thread, wire or line rising from the head or neck. Palette: mountain-stone greys, dark indigo cloth, dull brass fittings, plus the one accent named in the subject.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_command_signal_adjutant.png.
~~~

### 20. High Command Staff Tactician

References (download and attach, in this order):

1. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (it is an object, not a character; the figure is described entirely by the text): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_seal_charge.webp  (153182 bytes, 1174 x 1174, sha256 `6f56d9c84465f970…`)

~~~text
Draw ONE image for The Ninja RPG: High Command Staff Tactician. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (it is an object, not a character; the figure is described entirely by the text). Follow each reference only for its stated role.

Subject: High Command Staff Tactician: Division III. A tactician with a campaign map case under one arm and a brush wet with glowing chakra ink, the Grand Marshal's aide's cord on the shoulder. Accent: ink blue.

Continuity (Crownhold): a shinobi of the Skyglass Project's mountain fortress, recalled as a chakra impression. Dress him in the same outfit language as the style reference's crew: practical ninja gear (dark indigo and stone-grey cloth, rope and leather wraps, plain lacquered plates and bracers, a cloth mask or headwrap over the face), worn and weathered, solid and grounded. The only sign he is an impression: eyes lit with pale chakra and a faint chakra haze at the cloth's ragged edges. No glowing seams or veins, no translucent or crystal body, no gold filigree, no tassels, no crown, no technology. Closed boots or wrapped tabi footwear, no bare toes. No thread, wire or line rising from the head or neck. Palette: mountain-stone greys, dark indigo cloth, dull brass fittings, plus the one accent named in the subject.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_high_command_staff_tactician.png.
~~~

### 21. Honor Guard Commandant

References (download and attach, in this order):

1. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (it is an object, not a character; the figure is described entirely by the text): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_seal_charge.webp  (153182 bytes, 1174 x 1174, sha256 `6f56d9c84465f970…`)

~~~text
Draw ONE image for The Ninja RPG: Honor Guard Commandant. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (it is an object, not a character; the figure is described entirely by the text). Follow each reference only for its stated role.

Subject: Honor Guard Commandant: Division III. Ceremonial stone-grey lacquered plates and a tall tower shield bearing a plain circled-cross seal. Accent: polished brass.

Continuity (Crownhold): a shinobi of the Skyglass Project's mountain fortress, recalled as a chakra impression. Dress him in the same outfit language as the style reference's crew: practical ninja gear (dark indigo and stone-grey cloth, rope and leather wraps, plain lacquered plates and bracers, a cloth mask or headwrap over the face), worn and weathered, solid and grounded. The only sign he is an impression: eyes lit with pale chakra and a faint chakra haze at the cloth's ragged edges. No glowing seams or veins, no translucent or crystal body, no gold filigree, no tassels, no crown, no technology. Closed boots or wrapped tabi footwear, no bare toes. No thread, wire or line rising from the head or neck. Palette: mountain-stone greys, dark indigo cloth, dull brass fittings, plus the one accent named in the subject.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_honor_guard_commandant.png.
~~~

### 22. Strategist's Aide-de-Camp

References (download and attach, in this order):

1. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (it is an object, not a character; the figure is described entirely by the text): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_seal_charge.webp  (153182 bytes, 1174 x 1174, sha256 `6f56d9c84465f970…`)

~~~text
Draw ONE image for The Ninja RPG: Strategist's Aide-de-Camp. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (it is an object, not a character; the figure is described entirely by the text). Follow each reference only for its stated role.

Subject: Strategist's Aide-de-Camp: Division III. Sealed dispatch tubes on the back crackling with lightning chakra, light lacquered armour, an aide's sash. Accent: lightning white.

Continuity (Crownhold): a shinobi of the Skyglass Project's mountain fortress, recalled as a chakra impression. Dress him in the same outfit language as the style reference's crew: practical ninja gear (dark indigo and stone-grey cloth, rope and leather wraps, plain lacquered plates and bracers, a cloth mask or headwrap over the face), worn and weathered, solid and grounded. The only sign he is an impression: eyes lit with pale chakra and a faint chakra haze at the cloth's ragged edges. No glowing seams or veins, no translucent or crystal body, no gold filigree, no tassels, no crown, no technology. Closed boots or wrapped tabi footwear, no bare toes. No thread, wire or line rising from the head or neck. Palette: mountain-stone greys, dark indigo cloth, dull brass fittings, plus the one accent named in the subject.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_strategists_aide_de_camp.png.
~~~

### 23. Sanctum Vanguard

References (download and attach, in this order):

1. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (it is an object, not a character; the figure is described entirely by the text): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_seal_charge.webp  (153182 bytes, 1174 x 1174, sha256 `6f56d9c84465f970…`)

~~~text
Draw ONE image for The Ninja RPG: Sanctum Vanguard. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (it is an object, not a character; the figure is described entirely by the text). Follow each reference only for its stated role.

Subject: Sanctum Vanguard: Division IV. Obsidian-black lacquered plates, fire-chakra gauntlets ablaze, a short banner pole on the back. Accent: ember red.

Continuity (Crownhold): a shinobi of the Skyglass Project's mountain fortress, recalled as a chakra impression. Dress him in the same outfit language as the style reference's crew: practical ninja gear (dark indigo and stone-grey cloth, rope and leather wraps, plain lacquered plates and bracers, a cloth mask or headwrap over the face), worn and weathered, solid and grounded. The only sign he is an impression: eyes lit with pale chakra and a faint chakra haze at the cloth's ragged edges. No glowing seams or veins, no translucent or crystal body, no gold filigree, no tassels, no crown, no technology. Closed boots or wrapped tabi footwear, no bare toes. No thread, wire or line rising from the head or neck. Palette: mountain-stone greys, dark indigo cloth, dull brass fittings, plus the one accent named in the subject.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_sanctum_vanguard.png.
~~~

### 24. Directive Herald

References (download and attach, in this order):

1. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (it is an object, not a character; the figure is described entirely by the text): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_seal_charge.webp  (153182 bytes, 1174 x 1174, sha256 `6f56d9c84465f970…`)

~~~text
Draw ONE image for The Ninja RPG: Directive Herald. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (it is an object, not a character; the figure is described entirely by the text). Follow each reference only for its stated role.

Subject: Directive Herald: Division IV. Long dark ceremonial robes, an unrolled scroll of orders in one hand marked with glowing unreadable marks, lightning-lit eyes. Accent: lightning gold.

Continuity (Crownhold): a shinobi of the Skyglass Project's mountain fortress, recalled as a chakra impression. Dress him in the same outfit language as the style reference's crew: practical ninja gear (dark indigo and stone-grey cloth, rope and leather wraps, plain lacquered plates and bracers, a cloth mask or headwrap over the face), worn and weathered, solid and grounded. The only sign he is an impression: eyes lit with pale chakra and a faint chakra haze at the cloth's ragged edges. No glowing seams or veins, no translucent or crystal body, no gold filigree, no tassels, no crown, no technology. Closed boots or wrapped tabi footwear, no bare toes. No thread, wire or line rising from the head or neck. Palette: mountain-stone greys, dark indigo cloth, dull brass fittings, plus the one accent named in the subject.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_directive_herald.png.
~~~

### 25. Last Watch Executor

References (download and attach, in this order):

1. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (it is an object, not a character; the figure is described entirely by the text): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_seal_charge.webp  (153182 bytes, 1174 x 1174, sha256 `6f56d9c84465f970…`)

~~~text
Draw ONE image for The Ninja RPG: Last Watch Executor. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (it is an object, not a character; the figure is described entirely by the text). Follow each reference only for its stated role.

Subject: Last Watch Executor: Division IV. A tattered night-watch cloak, twin wind glaives, a blank mask stamped with an unreadable seal. Accent: night blue.

Continuity (Crownhold): a shinobi of the Skyglass Project's mountain fortress, recalled as a chakra impression. Dress him in the same outfit language as the style reference's crew: practical ninja gear (dark indigo and stone-grey cloth, rope and leather wraps, plain lacquered plates and bracers, a cloth mask or headwrap over the face), worn and weathered, solid and grounded. The only sign he is an impression: eyes lit with pale chakra and a faint chakra haze at the cloth's ragged edges. No glowing seams or veins, no translucent or crystal body, no gold filigree, no tassels, no crown, no technology. Closed boots or wrapped tabi footwear, no bare toes. No thread, wire or line rising from the head or neck. Palette: mountain-stone greys, dark indigo cloth, dull brass fittings, plus the one accent named in the subject.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_last_watch_executor.png.
~~~

### 26. Order-Bearer of the Sanctum

References (download and attach, in this order):

1. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (it is an object, not a character; the figure is described entirely by the text): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_seal_charge.webp  (153182 bytes, 1174 x 1174, sha256 `6f56d9c84465f970…`)

~~~text
Draw ONE image for The Ninja RPG: Order-Bearer of the Sanctum. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (it is an object, not a character; the figure is described entirely by the text). Follow each reference only for its stated role.

Subject: Order-Bearer of the Sanctum: Division IV. Deep-blue Sanctum wraps, a sealed scroll case, a blank command seal tablet held up. Accent: deep-sea blue.

Continuity (Crownhold): a shinobi of the Skyglass Project's mountain fortress, recalled as a chakra impression. Dress him in the same outfit language as the style reference's crew: practical ninja gear (dark indigo and stone-grey cloth, rope and leather wraps, plain lacquered plates and bracers, a cloth mask or headwrap over the face), worn and weathered, solid and grounded. The only sign he is an impression: eyes lit with pale chakra and a faint chakra haze at the cloth's ragged edges. No glowing seams or veins, no translucent or crystal body, no gold filigree, no tassels, no crown, no technology. Closed boots or wrapped tabi footwear, no bare toes. No thread, wire or line rising from the head or neck. Palette: mountain-stone greys, dark indigo cloth, dull brass fittings, plus the one accent named in the subject.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_order_bearer_of_the_sanctum.png.
~~~

### 27. Scene: Crownhold gate

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp  (250006 bytes, 1536 x 1024, sha256 `babd22ccf728fb67…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp  (85260 bytes, 728 x 728, sha256 `60087ce9e1d64019…`)

~~~text
Draw ONE image for The Ninja RPG: Scene: Crownhold gate. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: A snow-drifted parade ground before an open gate cut into a mountain wall; the gate stands open and unguarded; no banners; deep, unbroken snow; faint cyan light deep inside. (Used by: the fail node, 'you wake outside the gate in the snow'.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_crownhold_gate.png.
~~~

### 28. Scene: Armory proving hall

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp  (250006 bytes, 1536 x 1024, sha256 `babd22ccf728fb67…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp  (85260 bytes, 728 x 728, sha256 `60087ce9e1d64019…`)

~~~text
Draw ONE image for The Ninja RPG: Scene: Armory proving hall. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: Inside the Experimental Armory: rows of weapon racks humming behind glass, a live-fire trial range with targets, a brass placard by the first rack, cold stone and military brass. (Used by: Division I opening, the Proving Proctor.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_crownhold_proving_hall.png.
~~~

### 29. Scene: Ordnance store

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp  (250006 bytes, 1536 x 1024, sha256 `babd22ccf728fb67…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp  (85260 bytes, 728 x 728, sha256 `60087ce9e1d64019…`)

~~~text
Draw ONE image for The Ninja RPG: Scene: Ordnance store. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: An open ordnance store past the trial range: a counter with a ledger, shelves of sealed explosive tags glowing with heat, scorch marks on the stone. (Used by: the Ordnance Quartermaster.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_crownhold_ordnance_store.png.
~~~

### 30. Scene: Test gallery

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp  (250006 bytes, 1536 x 1024, sha256 `babd22ccf728fb67…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp  (85260 bytes, 728 x 728, sha256 `60087ce9e1d64019…`)

~~~text
Draw ONE image for The Ninja RPG: Scene: Test gallery. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: A narrow test gallery: an empty heavy firing rig bolted to the floor with lightning-scorched clamps and capacitor cables, crackling yellow sparks. (Used by: the Prototype Lancer Unit.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_crownhold_test_gallery.png.
~~~

### 31. Scene: Armory command terminal

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp  (250006 bytes, 1536 x 1024, sha256 `babd22ccf728fb67…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp  (85260 bytes, 728 x 728, sha256 `60087ce9e1d64019…`)

~~~text
Draw ONE image for The Ninja RPG: Scene: Armory command terminal. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: A glowing Military Command Terminal set into the armory wall beside a sealed door, a maintenance crawlway hatch behind live-fire racks with a three-switch lock. (Used by: Division I terminal, puzzle, protocols.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_crownhold_armory_terminal.png.
~~~

### 32. Scene: Forge wall

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp  (250006 bytes, 1536 x 1024, sha256 `babd22ccf728fb67…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp  (85260 bytes, 728 x 728, sha256 `60087ce9e1d64019…`)

~~~text
Draw ONE image for The Ninja RPG: Scene: Forge wall. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: The armory's heart: a towering forge wall hung with every weapon type ever tested, a glowing forge, an anvil, sealed door behind. (Used by: the Master of Arms.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_crownhold_forge_wall.png.
~~~

### 33. Scene: Archive of impressions

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp  (250006 bytes, 1536 x 1024, sha256 `babd22ccf728fb67…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp  (85260 bytes, 728 x 728, sha256 `60087ce9e1d64019…`)

~~~text
Draw ONE image for The Ninja RPG: Scene: Archive of impressions. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: A library of glass: tall shelves of crystal cores, each holding a faint sleeping light, cold blue air, a reading desk with an open ledger. (Used by: Division II opening, the Archive Keeper.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_crownhold_archive_of_impressions.png.
~~~

### 34. Scene: Vat halls

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp  (250006 bytes, 1536 x 1024, sha256 `babd22ccf728fb67…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp  (85260 bytes, 728 x 728, sha256 `60087ce9e1d64019…`)

~~~text
Draw ONE image for The Ninja RPG: Scene: Vat halls. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: Halls of tall glowing specimen tanks lit by one tall Skyglass lamp column; chains of vat keys on hooks; one tank cracked and dark. (Used by: the Containment Warden, the Unstable Echo Subject.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_crownhold_vat_halls.png.
~~~

### 35. Scene: Research command terminal

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp  (250006 bytes, 1536 x 1024, sha256 `babd22ccf728fb67…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp  (85260 bytes, 728 x 728, sha256 `60087ce9e1d64019…`)

~~~text
Draw ONE image for The Ninja RPG: Scene: Research command terminal. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: A command terminal beside the door of the reconstruction theatre, a plaque on the door, a locked maintenance stair behind the specimen tanks. (Used by: Division II terminal, puzzle, protocols.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_crownhold_research_terminal.png.
~~~

### 36. Scene: Reconstruction theatre

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp  (250006 bytes, 1536 x 1024, sha256 `babd22ccf728fb67…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp  (85260 bytes, 728 x 728, sha256 `60087ce9e1d64019…`)

~~~text
Draw ONE image for The Ninja RPG: Scene: Reconstruction theatre. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: An operating theatre seen from behind observation glass: a central operating floor ringed by tiered seats, a reconstruction rig of light and crystal over an empty table. (Used by: Replicant Zero.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_crownhold_reconstruction_theatre.png.
~~~

### 37. Scene: High Command signal room

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp  (250006 bytes, 1536 x 1024, sha256 `babd22ccf728fb67…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp  (85260 bytes, 728 x 728, sha256 `60087ce9e1d64019…`)

~~~text
Draw ONE image for The Ninja RPG: Scene: High Command signal room. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: A signal room: a long relay board of brass switches and paper tape, a sheet of paper printing itself line by line, maps of borders that no longer exist on the walls; empty of people. (Used by: Division III opening, the Signal Adjutant, and the aftermath; whoever sends the order is NEVER shown.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_crownhold_signal_room.png.
~~~

### 38. Scene: Planning hall

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp  (250006 bytes, 1536 x 1024, sha256 `babd22ccf728fb67…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp  (85260 bytes, 728 x 728, sha256 `60087ce9e1d64019…`)

~~~text
Draw ONE image for The Ninja RPG: Scene: Planning hall. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: A planning hall set for a war council no one will attend: a long table with campaign maps, empty chairs, an inkwell of glowing chakra ink. (Used by: the Staff Tactician.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_crownhold_planning_hall.png.
~~~

### 39. Scene: Honor guard corridor

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp  (250006 bytes, 1536 x 1024, sha256 `babd22ccf728fb67…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp  (85260 bytes, 728 x 728, sha256 `60087ce9e1d64019…`)

~~~text
Draw ONE image for The Ninja RPG: Scene: Honor guard corridor. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: A long corridor lined with suits of ceremonial stone-plated armour on stands, a tower shield with a plain circled-cross seal, leading to a closed office door. (Used by: the Honor Guard Commandant.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_crownhold_honor_guard_corridor.png.
~~~

### 40. Scene: High Command terminal

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp  (250006 bytes, 1536 x 1024, sha256 `babd22ccf728fb67…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp  (85260 bytes, 728 x 728, sha256 `60087ce9e1d64019…`)

~~~text
Draw ONE image for The Ninja RPG: Scene: High Command terminal. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: A command terminal outside a senior officer's office door, a narrow service corridor beside it, dispatch tubes on a rack. (Used by: Division III terminal, puzzle, protocols.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_crownhold_high_command_terminal.png.
~~~

### 41. Scene: The Grand Marshal's office

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp  (250006 bytes, 1536 x 1024, sha256 `babd22ccf728fb67…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp  (85260 bytes, 728 x 728, sha256 `60087ce9e1d64019…`)

~~~text
Draw ONE image for The Ninja RPG: Scene: The Grand Marshal's office. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: A severe, unadorned office: a folding map table, a single chair, a window onto snow, thirty years of annotated orders pinned to the wall. (Used by: the Grand Marshal.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_crownhold_marshals_office.png.
~~~

### 42. Scene: Sanctum gate

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp  (250006 bytes, 1536 x 1024, sha256 `babd22ccf728fb67…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp  (85260 bytes, 728 x 728, sha256 `60087ce9e1d64019…`)

~~~text
Draw ONE image for The Ninja RPG: Scene: Sanctum gate. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: The summit: a gate of dark obsidian lit by ember light at the top of a long stair, ember braziers, the Supreme Command banner. (Used by: Division IV opening, the Sanctum Vanguard.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_crownhold_sanctum_gate.png.
~~~

### 43. Scene: Sanctum antechamber

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp  (250006 bytes, 1536 x 1024, sha256 `babd22ccf728fb67…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp  (85260 bytes, 728 x 728, sha256 `60087ce9e1d64019…`)

~~~text
Draw ONE image for The Ninja RPG: Scene: Sanctum antechamber. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: An obsidian antechamber with a lectern for a herald's scroll, lightning-blue light on black stone, ember lamps. (Used by: the Directive Herald.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_crownhold_antechamber.png.
~~~

### 44. Scene: Outer ring and terminal

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp  (250006 bytes, 1536 x 1024, sha256 `babd22ccf728fb67…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp  (85260 bytes, 728 x 728, sha256 `60087ce9e1d64019…`)

~~~text
Draw ONE image for The Ninja RPG: Scene: Outer ring and terminal. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: The curved night-watch corridor of the Sanctum's outer ring, the last Military Command Terminal glowing in the wall, a sealed door ahead, a maintenance channel grille in the floor. (Used by: the Last Watch Executor, Division IV terminal, puzzle, protocols.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_crownhold_outer_ring.png.
~~~

### 45. Scene: Throne room

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp  (250006 bytes, 1536 x 1024, sha256 `babd22ccf728fb67…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp  (85260 bytes, 728 x 728, sha256 `60087ce9e1d64019…`)

~~~text
Draw ONE image for The Ninja RPG: Scene: Throne room. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: An obsidian throne room lit by ember light, a tall summit window looking out over a whole mountain range at night, an empty command seat; faint cyan threads of light run from the floor up toward where the commander stands (he is not shown). (Used by: Supreme Commander Arakane.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_crownhold_throne_room.png.
~~~

### 46. The Last Directive (jutsu icon)

References (download and attach, in this order):

1. STYLE: jutsu icon register: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/style_refs/jutsu_icons/bbe/icon_bbe_sapphire_command_v2.webp  (61270 bytes, 256 x 256, sha256 `410b8c5a20af40b2…`)
2. MOTIF: the Command Crown: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/crownhold/avatar_crownhold_arakane.webp  (289646 bytes, 1239 x 1239, sha256 `0383691812dc3467…`)

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

1. STYLE: jutsu icon register: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/style_refs/jutsu_icons/bbe/icon_bbe_sapphire_command_v2.webp  (61270 bytes, 256 x 256, sha256 `410b8c5a20af40b2…`)
2. MOTIF: the Command Crown: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/crownhold/avatar_crownhold_arakane.webp  (289646 bytes, 1239 x 1239, sha256 `0383691812dc3467…`)

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

1. SUBJECT AND PIXEL STYLE: the seal tablet at Arakane's belt: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/crownhold/avatar_crownhold_arakane.webp  (289646 bytes, 1239 x 1239, sha256 `0383691812dc3467…`)

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

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/skyglass_event_icons/exports/icon-skyglass-coffer.webp  (70574 bytes, 256 x 256, sha256 `a7bbfe7e60570aef…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/crownhold/avatar_crownhold_arakane.webp  (289646 bytes, 1239 x 1239, sha256 `0383691812dc3467…`)

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

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/skyglass_event_icons/exports/icon-tool-pouch-katon.webp  (67920 bytes, 256 x 256, sha256 `b1fa26ced2204d1e…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/crownhold/avatar_crownhold_arakane.webp  (289646 bytes, 1239 x 1239, sha256 `0383691812dc3467…`)

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

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/skyglass_event_icons/exports/icon-tool-pouch-wave.webp  (67620 bytes, 256 x 256, sha256 `44fa5437a835a3e0…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/crownhold/avatar_crownhold_arakane.webp  (289646 bytes, 1239 x 1239, sha256 `0383691812dc3467…`)

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

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/skyglass_event_icons/exports/icon-tool-pouch-ikazuchi.webp  (68698 bytes, 256 x 256, sha256 `c644532a96cbf44e…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/crownhold/avatar_crownhold_arakane.webp  (289646 bytes, 1239 x 1239, sha256 `0383691812dc3467…`)

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

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/skyglass_event_icons/exports/icon-tool-pouch-stonefall.webp  (68232 bytes, 256 x 256, sha256 `029a560a5bcbc202…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/crownhold/avatar_crownhold_arakane.webp  (289646 bytes, 1239 x 1239, sha256 `0383691812dc3467…`)

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

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/skyglass_event_icons/exports/icon-tool-pouch-zephyrfang.webp  (66358 bytes, 256 x 256, sha256 `ca3d144715e8385b…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/crownhold/avatar_crownhold_arakane.webp  (289646 bytes, 1239 x 1239, sha256 `0383691812dc3467…`)

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

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/skyglass_event_icons/exports/icon-chart-drowned-foundry.webp  (60940 bytes, 256 x 256, sha256 `0b00806939bd375a…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/crownhold/avatar_crownhold_arakane.webp  (289646 bytes, 1239 x 1239, sha256 `0383691812dc3467…`)

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

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/skyglass_event_icons/exports/icon-chart-quarantined-archive.webp  (65754 bytes, 256 x 256, sha256 `80df641bad0135e7…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/crownhold/avatar_crownhold_arakane.webp  (289646 bytes, 1239 x 1239, sha256 `0383691812dc3467…`)

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

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/skyglass_event_icons/exports/icon-chart-captains-watch.webp  (68722 bytes, 256 x 256, sha256 `e576a50a3f066e97…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/crownhold/avatar_crownhold_arakane.webp  (289646 bytes, 1239 x 1239, sha256 `0383691812dc3467…`)

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

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/skyglass_event_icons/exports/icon-skyglass-signal-beacon.webp  (45678 bytes, 256 x 256, sha256 `6b58863e0d526502…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/crownhold/avatar_crownhold_arakane.webp  (289646 bytes, 1239 x 1239, sha256 `0383691812dc3467…`)

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

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/skyglass_event_icons/exports/icon-armory-requisition.webp  (47944 bytes, 256 x 256, sha256 `869b66de517273ad…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/crownhold/avatar_crownhold_arakane.webp  (289646 bytes, 1239 x 1239, sha256 `0383691812dc3467…`)

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

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/icon_ghost_ship_skyglass_crown.webp  (116290 bytes, 480 x 480, sha256 `02cde28f5fedfaf3…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/crownhold/avatar_crownhold_arakane.webp  (289646 bytes, 1239 x 1239, sha256 `0383691812dc3467…`)

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

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/icon_ghost_ship_skyglass_crown_fragment.webp  (107374 bytes, 480 x 480, sha256 `434872cd478550ca…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/crownhold/avatar_crownhold_arakane.webp  (289646 bytes, 1239 x 1239, sha256 `0383691812dc3467…`)

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

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/icon_ghost_ship_skyglass_crystal.webp  (103342 bytes, 480 x 480, sha256 `896543c69115e830…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/crownhold/avatar_crownhold_arakane.webp  (289646 bytes, 1239 x 1239, sha256 `0383691812dc3467…`)

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

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/icon_ghost_ship_skyglass_filament.webp  (129168 bytes, 480 x 480, sha256 `b165dba7e5849bcd…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/crownhold/avatar_crownhold_arakane.webp  (289646 bytes, 1239 x 1239, sha256 `0383691812dc3467…`)

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

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/icon_ghost_ship_skyglass_katana.webp  (56510 bytes, 480 x 480, sha256 `f7a336ca9fc0067a…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/crownhold/avatar_crownhold_arakane.webp  (289646 bytes, 1239 x 1239, sha256 `0383691812dc3467…`)

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

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/icon_ghost_ship_skyglass_serum.webp  (277032 bytes, 768 x 768, sha256 `6d83e870aa4bdbd8…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/crownhold/avatar_crownhold_arakane.webp  (289646 bytes, 1239 x 1239, sha256 `0383691812dc3467…`)

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

1. COMPOSITION AND COLOUR base (painted: redraw, do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_exterior_keel_walk.webp  (224364 bytes, 1536 x 1024, sha256 `f665ca4bb8bc4da0…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp  (85260 bytes, 728 x 728, sha256 `60087ce9e1d64019…`)

~~~text
Draw ONE image for The Ninja RPG: Scene: Wreck keel and hatch. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COMPOSITION AND COLOUR base (painted: redraw, do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: Use the first reference as the starting composition and colour, changed to match this brief exactly: Outside the beached Skyglass warship at night: its split keel lies on wet sand and dark rocks at the waterline, iron bands and timber looming overhead; glowing pale cyan seal channels run along the hull into a low hatch rimmed with cooled crystal, and seawater pours past the hatch into the dark below. (Used by: Drowned Foundry d_arrive; Quarantined Archive d_arrive.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_skyglass_wreck_keel.png.
~~~

### 67. Scene: Flooded intake

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (painted: do not copy its rendering or layout): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_lower_hull.webp  (443164 bytes, 1536 x 1024, sha256 `5906fa63576bb878…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp  (85260 bytes, 728 x 728, sha256 `60087ce9e1d64019…`)

~~~text
Draw ONE image for The Ninja RPG: Scene: Flooded intake. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (painted: do not copy its rendering or layout); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: A new location: The foundry's intake hall inside the wreck, half flooded: dark water at knee height, empty seal canisters bobbing against the walls, iron pipes and valve wheels, pale cyan light glinting off the water. (Used by: Drowned Foundry d_intake, b_intake.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_skyglass_foundry_intake.png.
~~~

### 68. Scene: Cooling racks

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (painted: do not copy its rendering or layout): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_hold.webp  (311832 bytes, 1536 x 1024, sha256 `6743482693564c43…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp  (85260 bytes, 728 x 728, sha256 `60087ce9e1d64019…`)

~~~text
Draw ONE image for The Ninja RPG: Scene: Cooling racks. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (painted: do not copy its rendering or layout); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: A new location: A long hall of iron cooling racks stacked with freshly cast, glowing pale cyan Skyglass ingots that no one has collected; water at ankle height across the floor; a sealed hatch high on the far wall. (Used by: Drowned Foundry d_racks.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_skyglass_foundry_racks.png.
~~~

### 69. Scene: Pour hall

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (painted: do not copy its rendering or layout): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_lower_hull.webp  (443164 bytes, 1536 x 1024, sha256 `5906fa63576bb878…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp  (85260 bytes, 728 x 728, sha256 `60087ce9e1d64019…`)

~~~text
Draw ONE image for The Ninja RPG: Scene: Pour hall. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (painted: do not copy its rendering or layout); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: A new location: The pour hall: rows of stone casting moulds wired together with seal charges, an inspector's ledger desk, knee-deep water, and an orange-white crucible glow coming up through iron floor grates from below. (Used by: Drowned Foundry d_hall, b_hall, d_gate.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_skyglass_foundry_pour_hall.png.
~~~

### 70. Scene: Crucible chamber

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (painted: do not copy its rendering or layout): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_hold.webp  (311832 bytes, 1536 x 1024, sha256 `6743482693564c43…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp  (85260 bytes, 728 x 728, sha256 `60087ce9e1d64019…`)

~~~text
Draw ONE image for The Ninja RPG: Scene: Crucible chamber. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (painted: do not copy its rendering or layout); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: A new location: The crucible chamber, the only dry room in the works, kept dry by heat: a great tilting crucible of molten pale cyan Skyglass hung in heavy pouring gear, glowing moulds, steam rising where water seeps in at the edges. (Used by: Drowned Foundry d_crucible, b_warden, d_pour.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_skyglass_foundry_crucible.png.
~~~

### 71. Scene: Rebuilding lower hull

References (download and attach, in this order):

1. COMPOSITION AND COLOUR base (painted: redraw, do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_lower_hull.webp  (443164 bytes, 1536 x 1024, sha256 `5906fa63576bb878…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp  (85260 bytes, 728 x 728, sha256 `60087ce9e1d64019…`)

~~~text
Draw ONE image for The Ninja RPG: Scene: Rebuilding lower hull. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COMPOSITION AND COLOUR base (painted: redraw, do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: Use the first reference as the starting composition and colour, changed to match this brief exactly: Below the waterline inside the wreck: the hull is rebuilding itself out of timber and cable that do not belong together, half-formed frames knitting in pale cyan seal light; a ladder down to a severed, pulsing conduit. (Used by: Quarantined Archive d_hull, b_horror, d_conduit.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_skyglass_lower_hull.png.
~~~

### 72. Scene: Reconstruction chamber

References (download and attach, in this order):

1. COMPOSITION AND COLOUR base (painted: redraw, do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_reconstruction_chamber.webp  (446336 bytes, 1470 x 980, sha256 `d0b0c3297409638c…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp  (85260 bytes, 728 x 728, sha256 `60087ce9e1d64019…`)

~~~text
Draw ONE image for The Ninja RPG: Scene: Reconstruction chamber. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COMPOSITION AND COLOUR base (painted: redraw, do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: Use the first reference as the starting composition and colour, changed to match this brief exactly: Rows of empty upright frames, each holding a faint human impression in seal light; a three-way seal plate in the centre of the floor. (Used by: Quarantined Archive d_chamber, d_seal1, d_alarm1, b_alarm1.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_skyglass_reconstruction_chamber.png.
~~~

### 73. Scene: Quarantined archive

References (download and attach, in this order):

1. COMPOSITION AND COLOUR base (painted: redraw, do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_quarantined_archive.webp  (344950 bytes, 1536 x 1024, sha256 `25682147baa0fd69…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp  (85260 bytes, 728 x 728, sha256 `60087ce9e1d64019…`)

~~~text
Draw ONE image for The Ninja RPG: Scene: Quarantined archive. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COMPOSITION AND COLOUR base (painted: redraw, do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: Use the first reference as the starting composition and colour, changed to match this brief exactly: A narrow sealed archive not on any ship plan: tall index shelves of command records and route sheets, a handle-less door crossed with pale script, containment seals on every cabinet. (Used by: Quarantined Archive d_seal2 onward, alarms 2-3, the Sealwright.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_skyglass_quarantined_archive.png.
~~~

### 74. Scene: Night cove landing

References (download and attach, in this order):

1. COMPOSITION AND COLOUR base (painted: redraw, do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_cache_site.webp  (156820 bytes, 1536 x 1024, sha256 `4ad71d71d9794353…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp  (85260 bytes, 728 x 728, sha256 `60087ce9e1d64019…`)

~~~text
Draw ONE image for The Ninja RPG: Scene: Night cove landing. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COMPOSITION AND COLOUR base (painted: redraw, do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: Use the first reference as the starting composition and colour, changed to match this brief exactly: A quiet cove at night under a full moon: the Ghost Ship's longboat drawn up on the sand, oars shipped, a lantern on its bow; dark water and the silhouette of the wreck's masts beyond the headland. (Used by: Captain's Watch d_landing.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_skyglass_cove_landing.png.
~~~

### 75. Scene: Chart room

References (download and attach, in this order):

1. COMPOSITION AND COLOUR base (painted: redraw, do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_chart_room.webp  (378286 bytes, 1536 x 1024, sha256 `ed6ae32d26e8b586…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp  (85260 bytes, 728 x 728, sha256 `60087ce9e1d64019…`)

~~~text
Draw ONE image for The Ninja RPG: Scene: Chart room. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COMPOSITION AND COLOUR base (painted: redraw, do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: Use the first reference as the starting composition and colour, changed to match this brief exactly: The ship's chart room: a big table buried in charts layered with decades of corrections, route pins and dividers, glowing pale cyan route lines redrawn over older ink. (Used by: Captain's Watch fight 1 (Wayfinder).)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_skyglass_chart_room.png.
~~~

### 76. Scene: Open deck in a gale

References (download and attach, in this order):

1. COMPOSITION AND COLOUR base (painted: redraw, do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_deck_b.webp  (355890 bytes, 1536 x 1024, sha256 `e6004e0ab8749afc…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp  (85260 bytes, 728 x 728, sha256 `60087ce9e1d64019…`)

~~~text
Draw ONE image for The Ninja RPG: Scene: Open deck in a gale. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COMPOSITION AND COLOUR base (painted: redraw, do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: Use the first reference as the starting composition and colour, changed to match this brief exactly: The open upper deck in a rising gale: torn sails cracking, rigging lines singing, empty mess tables lashed down, pale cyan seal light along the rails. (Used by: Captain's Watch fight 2 (First Blade).)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_skyglass_deck.png.
~~~

### 77. Scene: Helm and command dais

References (download and attach, in this order):

1. COMPOSITION AND COLOUR base (painted: redraw, do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_helm.webp  (329520 bytes, 1536 x 1024, sha256 `d72d0506b07b59a9…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp  (85260 bytes, 728 x 728, sha256 `60087ce9e1d64019…`)

~~~text
Draw ONE image for The Ninja RPG: Scene: Helm and command dais. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COMPOSITION AND COLOUR base (painted: redraw, do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: Use the first reference as the starting composition and colour, changed to match this brief exactly: The raised command dais at the helm: the great wheel, core-link seals glowing pale cyan in the floor, the ship's seal sigil on a banner, night sky beyond. (Used by: Captain's Watch fight 3 (the Captain).)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_skyglass_helm.png.
~~~

### 78. Scene: Observation gallery

References (download and attach, in this order):

1. COMPOSITION AND COLOUR base (painted: redraw, do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp  (250006 bytes, 1536 x 1024, sha256 `babd22ccf728fb67…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp  (85260 bytes, 728 x 728, sha256 `60087ce9e1d64019…`)

~~~text
Draw ONE image for The Ninja RPG: Scene: Observation gallery. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COMPOSITION AND COLOUR base (painted: redraw, do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: Use the first reference as the starting composition and colour, changed to match this brief exactly: A viewing gallery above the command deck: tall windows showing the whole ship's glowing seal network repairing itself, storage chests along the walls. (Used by: Captain's Watch endings.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_skyglass_observation_gallery.png.
~~~

### 79. Scene: Three coves and the stone shrine

References (download and attach, in this order):

1. COMPOSITION AND COLOUR base (painted: redraw, do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_cache_site.webp  (156820 bytes, 1536 x 1024, sha256 `4ad71d71d9794353…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp  (85260 bytes, 728 x 728, sha256 `60087ce9e1d64019…`)

~~~text
Draw ONE image for The Ninja RPG: Scene: Three coves and the stone shrine. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COMPOSITION AND COLOUR base (painted: redraw, do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: Use the first reference as the starting composition and colour, changed to match this brief exactly: A stretch of night shore with three small coves: a split cliff breaking the tide on the left, an open beach past a reef in the middle, and on the right a small stone shrine on the cliff above a cove, its shadow falling across the sand where the cache is buried. (Used by: The Buried Cache, every node.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_skyglass_buried_cache_shore.png.
~~~

