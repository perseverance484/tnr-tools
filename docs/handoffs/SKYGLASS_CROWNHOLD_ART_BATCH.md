# Art batch: Skyglass event and Crownhold (79 images, plus prerequisite brief A)

- **Director, 2026-10-25:** "Draft up a design document for the art director to pull each prompt from and use references. Then a short compact hand off for each image in sequence and I hand you back the approved image."
- **Style (director, 2026-10-25):** every image in this batch is PREMIUM PIXEL ART, the same rendering as the Crownhold/crew avatars. Painted references (the Coffer, the charts, the jutsu exemplar) supply subject, materials and colours only. **Art bible v0.4 (proposed):** `docs/design/ghost_ship_art_bible/` (ART_BIBLE.md, blocks.json, roster.json); the original crew is the rendering anchor: the Deck Warden for characters, the Seal Charge for objects, the Captain's portrait for scenes. Arakane's gold avatar is off-model and is not a reference.
- **Protocol:** `docs/workflows/ISOLATED_ART_GENERATION.md`. One image per fresh session, at most two reference images (never a collage), one candidate at a time. The art director returns the RAW image; Claude Code keys, crops, exports and QCs it (`skills/producing-tnr-art`), then swaps the placeholder in game by manifest.
- **Pixel redraws (#36 to #46):** the event icons already live were painted; each is redrawn as pixel art from its own approved image so the whole set matches (director, 2026-10-25).
- **More pixel art (#47 onward):** the six Skyglass item icons inside the Coffer (redraws), then one scene per location the hunts actually depict (14; the wreck is now beached, and each Foundry room gets its own). Each scene lists the nodes that use it so the quests can be repointed when the art lands. Already pixel art and NOT redrawn: every crew avatar, the four scene portraits, the map structure. Left out: the retired Reliquary and old chests, and the retiring Ghost Ship quest icon.
- **Prerequisite A:** Supreme Commander Arakane redrawn to the v0.4 crown lock (iron ring, seven skyglass blades, no gold); #5 and #46-#48 are BLOCKED until it is approved. **Not in this batch:** the Sealwright and Oathkeeper scene portraits (already exist). **Deferred:** the Lastlight hit animation (a vertical strip sprite sheet; its placeholder is KGK: Black Fang Lance's).
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
| A | Supreme Commander Arakane | AI_AVATAR | magenta | deck_warden | `avatar_crownhold_arakane_v2.webp` |
| 1 | Sealed Treasury | ICON | lime | treasury_subject, arakane | `icon-sealed-treasury.webp` |
| 2 | Archive Chart Case | ICON | lime | foundry_chart, arakane | `icon-archive-chart-case.webp` |
| 3 | Chart of the Buried Cache | ICON | lime | foundry_chart, arakane | `icon-chart-buried-cache.webp` |
| 4 | Unmarked Cargo | ICON | lime | coffer, arakane | `icon-unmarked-cargo.webp` |
| 5 | Crownbreaker (badge) | ICON | magenta | seal_charge | `icon-badge-crownbreaker.webp` |
| 6 | Lastlight (jutsu icon) | JUTSU_ICON | none | bbe, lantern | `icon-jutsu-lastlight.webp` |
| 7 | Foundry Warden (AI avatar) | AI_AVATAR | magenta | deck_warden | `avatar_skyglass_foundry_warden.webp` |
| 8 | Armsmaster (commander) | AI_AVATAR | magenta | deck_warden | `avatar_crownhold_master_of_arms.webp` |
| 9 | Replicant Zero (commander) | AI_AVATAR | magenta | deck_warden | `avatar_crownhold_replicant_zero.webp` |
| 10 | The Second (commander) | AI_AVATAR | magenta | deck_warden | `avatar_crownhold_the_grand_marshal.webp` |
| 11 | Trialmaster | AI_AVATAR | magenta | deck_warden | `avatar_crownhold_proving_proctor.webp` |
| 12 | Tagwright | AI_AVATAR | magenta | deck_warden | `avatar_crownhold_ordnance_quartermaster.webp` |
| 13 | Lancer | AI_AVATAR | magenta | deck_warden | `avatar_crownhold_prototype_lancer_unit.webp` |
| 14 | Duelist | AI_AVATAR | magenta | deck_warden | `avatar_crownhold_calibration_duelist.webp` |
| 15 | Archivist | AI_AVATAR | magenta | deck_warden | `avatar_crownhold_skyglass_archive_keeper.webp` |
| 16 | Binder | AI_AVATAR | magenta | deck_warden | `avatar_crownhold_impression_containment_warden.webp` |
| 17 | Echo | AI_AVATAR | magenta | deck_warden | `avatar_crownhold_unstable_echo_subject.webp` |
| 18 | Stonebound | AI_AVATAR | magenta | deck_warden | `avatar_crownhold_failed_reconstruction_prototype.webp` |
| 19 | Signaller | AI_AVATAR | magenta | deck_warden | `avatar_crownhold_command_signal_adjutant.webp` |
| 20 | Tactician | AI_AVATAR | magenta | deck_warden | `avatar_crownhold_high_command_staff_tactician.webp` |
| 21 | Honor Guard | AI_AVATAR | magenta | deck_warden | `avatar_crownhold_honor_guard_commandant.webp` |
| 22 | Runner | AI_AVATAR | magenta | deck_warden | `avatar_crownhold_strategists_aide_de_camp.webp` |
| 23 | Vanguard | AI_AVATAR | magenta | deck_warden | `avatar_crownhold_sanctum_vanguard.webp` |
| 24 | Herald | AI_AVATAR | magenta | deck_warden | `avatar_crownhold_directive_herald.webp` |
| 25 | Last Watch | AI_AVATAR | magenta | deck_warden | `avatar_crownhold_last_watch_executor.webp` |
| 26 | Sealbearer | AI_AVATAR | magenta | deck_warden | `avatar_crownhold_order_bearer_of_the_sanctum.webp` |
| 27 | Scene: Crownhold gate | SCENE_BACKGROUND | none | gallery, captain_portrait | `scene_bg_crownhold_gate.webp` |
| 28 | Scene: Armory proving hall | SCENE_BACKGROUND | none | gallery, captain_portrait | `scene_bg_crownhold_proving_hall.webp` |
| 29 | Scene: Ordnance store | SCENE_BACKGROUND | none | gallery, captain_portrait | `scene_bg_crownhold_ordnance_store.webp` |
| 30 | Scene: Test gallery | SCENE_BACKGROUND | none | gallery, captain_portrait | `scene_bg_crownhold_test_gallery.webp` |
| 31 | Scene: Armory command shrine | SCENE_BACKGROUND | none | gallery, captain_portrait | `scene_bg_crownhold_armory_terminal.webp` |
| 32 | Scene: Forge wall | SCENE_BACKGROUND | none | gallery, captain_portrait | `scene_bg_crownhold_forge_wall.webp` |
| 33 | Scene: Archive of impressions | SCENE_BACKGROUND | none | gallery, captain_portrait | `scene_bg_crownhold_archive_of_impressions.webp` |
| 34 | Scene: Sealing jar halls | SCENE_BACKGROUND | none | gallery, captain_portrait | `scene_bg_crownhold_vat_halls.webp` |
| 35 | Scene: Research command shrine | SCENE_BACKGROUND | none | gallery, captain_portrait | `scene_bg_crownhold_research_terminal.webp` |
| 36 | Scene: Recall chamber | SCENE_BACKGROUND | none | gallery, captain_portrait | `scene_bg_crownhold_reconstruction_theatre.webp` |
| 37 | Scene: High Command signal room | SCENE_BACKGROUND | none | gallery, captain_portrait | `scene_bg_crownhold_signal_room.webp` |
| 38 | Scene: Planning hall | SCENE_BACKGROUND | none | gallery, captain_portrait | `scene_bg_crownhold_planning_hall.webp` |
| 39 | Scene: Honor guard corridor | SCENE_BACKGROUND | none | gallery, captain_portrait | `scene_bg_crownhold_honor_guard_corridor.webp` |
| 40 | Scene: High Command shrine | SCENE_BACKGROUND | none | gallery, captain_portrait | `scene_bg_crownhold_high_command_terminal.webp` |
| 41 | Scene: The Second's office | SCENE_BACKGROUND | none | gallery, captain_portrait | `scene_bg_crownhold_marshals_office.webp` |
| 42 | Scene: Sanctum gate | SCENE_BACKGROUND | none | gallery, captain_portrait | `scene_bg_crownhold_sanctum_gate.webp` |
| 43 | Scene: Sanctum antechamber | SCENE_BACKGROUND | none | gallery, captain_portrait | `scene_bg_crownhold_antechamber.webp` |
| 44 | Scene: Outer ring and shrine | SCENE_BACKGROUND | none | gallery, captain_portrait | `scene_bg_crownhold_outer_ring.webp` |
| 45 | Scene: Throne room | SCENE_BACKGROUND | none | gallery, captain_portrait | `scene_bg_crownhold_throne_room.webp` |
| 46 | The Last Directive (jutsu icon) | JUTSU_ICON | none | bbe | `icon-jutsu-the-last-directive.webp` |
| 47 | Extermination Order (jutsu icon) | JUTSU_ICON | none | bbe | `icon-jutsu-extermination-order.webp` |
| 48 | Countermand (item icon) | ICON | lime | seal_charge | `icon-countermand.webp` |
| 49 | Skyglass Coffer (pixel redraw) | ICON | lime | redraw_icon-skyglass-coffer.webp, seal_charge | `icon-skyglass-coffer-pixel.webp` |
| 50 | Katon Tool Pouch (pixel redraw) | ICON | lime | redraw_icon-tool-pouch-katon.webp, seal_charge | `icon-tool-pouch-katon-pixel.webp` |
| 51 | Wave Tool Pouch (pixel redraw) | ICON | lime | redraw_icon-tool-pouch-wave.webp, seal_charge | `icon-tool-pouch-wave-pixel.webp` |
| 52 | Ikazuchi Tool Pouch (pixel redraw) | ICON | lime | redraw_icon-tool-pouch-ikazuchi.webp, seal_charge | `icon-tool-pouch-ikazuchi-pixel.webp` |
| 53 | Stonefall Tool Pouch (pixel redraw) | ICON | lime | redraw_icon-tool-pouch-stonefall.webp, seal_charge | `icon-tool-pouch-stonefall-pixel.webp` |
| 54 | Zephyrfang Tool Pouch (pixel redraw) | ICON | magenta | redraw_icon-tool-pouch-zephyrfang.webp, seal_charge | `icon-tool-pouch-zephyrfang-pixel.webp` |
| 55 | Chart of the Drowned Foundry (pixel redraw) | ICON | lime | redraw_icon-chart-drowned-foundry.webp, seal_charge | `icon-chart-drowned-foundry-pixel.webp` |
| 56 | Chart of the Quarantined Archive (pixel redraw) | ICON | lime | redraw_icon-chart-quarantined-archive.webp, seal_charge | `icon-chart-quarantined-archive-pixel.webp` |
| 57 | Chart of the Captain's Watch (pixel redraw) | ICON | lime | redraw_icon-chart-captains-watch.webp, seal_charge | `icon-chart-captains-watch-pixel.webp` |
| 58 | Lastlight Lantern (pixel redraw) | ICON | lime | redraw_icon-skyglass-signal-beacon.webp, seal_charge | `icon-skyglass-signal-beacon-pixel.webp` |
| 59 | Armory Requisition (pixel redraw) | ICON | lime | redraw_icon-armory-requisition.webp, seal_charge | `icon-armory-requisition-pixel.webp` |
| 60 | Skyglass Crown (pixel redraw) | ICON | lime | redraw_icon_ghost_ship_skyglass_crown.webp, seal_charge | `icon_ghost_ship_skyglass_crown_pixel.webp` |
| 61 | Skyglass Crown Fragment (pixel redraw) | ICON | lime | redraw_icon_ghost_ship_skyglass_crown_fragment.webp, seal_charge | `icon_ghost_ship_skyglass_crown_fragment_pixel.webp` |
| 62 | Skyglass Crystal (pixel redraw) | ICON | lime | redraw_icon_ghost_ship_skyglass_crystal.webp, seal_charge | `icon_ghost_ship_skyglass_crystal_pixel.webp` |
| 63 | Skyglass Filament (pixel redraw) | ICON | lime | redraw_icon_ghost_ship_skyglass_filament.webp, seal_charge | `icon_ghost_ship_skyglass_filament_pixel.webp` |
| 64 | Skyglass Katana (pixel redraw) | ICON | lime | redraw_icon_ghost_ship_skyglass_katana.webp, seal_charge | `icon_ghost_ship_skyglass_katana_pixel.webp` |
| 65 | Skyglass Serum (pixel redraw) | ICON | lime | redraw_icon_ghost_ship_skyglass_serum.webp, seal_charge | `icon_ghost_ship_skyglass_serum_pixel.webp` |
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

### A. Supreme Commander Arakane

> Prerequisite brief, outside the 79. Prerequisite for #5 and #46-#48. Replaces the gold design of avatar_crownhold_arakane.webp (kept as history; delivered under a new name).

References (download and attach, in this order):

1. STYLE: the original crew's look (rendering, palette, outline weight, outfit language and proportions); this is a different person, whose head, gear and weapons are described by the text: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_deck_warden.webp  (123206 bytes, 1221 x 1221, sha256 `805c1e99bcb1e7b3…`)

~~~text
Draw ONE image for The Ninja RPG: Supreme Commander Arakane. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: the original crew's look (rendering, palette, outline weight, outfit language and proportions); this is a different person, whose head, gear and weapons are described by the text. Follow each reference only for its stated role.

Subject: Supreme Commander Arakane: Crownhold, Division IV (Sanctum). Head: a plain dark hood, a severe iron half-mask, and the Command Crown described below. Weapon or prop: a single broad black-iron nagamaki. Stance: the tallest of all, lean and commanding, the blade held horizontal. The Command Crown: a thin CLOSED ring of blackened iron with seven blunt iron seal notches and one small faceted pale cyan seal stone at the front; above it, with a small gap, seven separate floating skyglass blades: one central upright blade, a pair of inner diagonals, a pair of outer diagonals and two shorter flanking blades; the crystal blades outlined dark and cel shaded in two or three steps. Crown constraints: no gold, no glowing strings or threads, no extra crystal debris, no jewels, no giant light halo, no radiant ghost body, no ornate armour. Keep: a long straight split haori; a controlled silhouette; outranks the Crowned Captain through disciplined seven-blade geometry and posture, not size or decoration; the crown reads as one powerful head silhouette at 125 px. Rank: a commander, about a tenth taller than a regular, NOT wider: a structured raised collar, a longer split haori, a controlled battle stance; no oversized shoulder plates, no gold; he alone wears the Command Crown, and he stands tallest of all. Division IV, Sanctum: a severe enclosed silhouette, the darkest clothing, straight seal panels, almost no accessories. Division material: pale iron-ash (#86858A) as a subdued, non-glowing cloth or lacquer shade on trim and panels; pale skyglass cyan stays the only luminous colour.

Style: Edo-era Japanese fantasy ninja, premium pixel art matching the original Skyglass crew in density and darkness: fine, deliberate pixel clusters, hard dark outlines about one art pixel wide, flat cel shading in two or three value steps per material, limited palette; no chunky retro sprite, no smoothing, no bloom, no airbrush. Colour: night-ink and deep indigo cloth, storm-grey iron, weathered leather; pale skyglass cyan only where it is materially there (eyes, a skyglass part, a chakra-worked edge); rope only for functional lashings and containers. Full body, eye level, front three-quarter view, inside the frame with a clear margin; grounded adult anatomy, readable at 125 px; both arms within the silhouette.
Costume (common crew language, not a uniform): Edo shinobi layered kimono, haori, hakama or fitted wraps; a cloth mask; a hood, headwrap or hat; an indigo waist sash; closed tabi with wrapped shins; practical arm protection; plain lacquered armour only where the subject asks for it, never ornate parade armour; torn hems and sash ends may show movement. The head described in the subject replaces these defaults. One dominant weapon or working tool. Solid gloved hands with five fingers.
He is a fully solid shinobi recalled as a chakra impression, with normal anatomy and equipment; the only signs are small chakra-lit eyes and a faint haze at the cloth's torn edges.
Chakra, if any, is compact and purposeful, at a working blade, tool or hand; no free-floating spell effects.
On a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no electronic or futuristic objects, no terminals, screens, cables, laboratory machinery or futuristic weapons, no transparent body, no floating limbs, no ghost hands, no glowing seams or veins, no crystal skin, no glitch effects, no threads or lines from the head, no gold, no filigree, no jewellery, no tassels, no second crown, no ornate parade armour, no headband, no forehead protector, no clan or village symbol, no text, no bare toes, no aura or halo, no rainbow accents, no realistic or smooth painterly rendering, no anime-scaled eyes, no blur, no scenery, no floor, no cast shadow on the key colour, no key-colour spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no sheet, no grid.

Return the raw image named raw_avatar_crownhold_arakane_v2.png.
~~~

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

> BLOCKED until brief A (the Arakane v2 avatar) is approved and committed; then rerun the builder and the approved avatar joins this image as its SUBJECT reference. Do not generate before that.

References (download and attach, in this order):

1. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (an object of the same crew): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_seal_charge.webp  (153182 bytes, 1174 x 1174, sha256 `6f56d9c84465f970…`)

~~~text
Draw ONE image for The Ninja RPG: Crownbreaker (badge). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (an object of the same crew). Follow each reference only for its stated role.

Subject: Crownbreaker: Supreme Commander Arakane's Command Crown at the moment it breaks. The Command Crown: a thin CLOSED ring of blackened iron with seven blunt iron seal notches and one small faceted pale cyan seal stone at the front; above it, with a small gap, seven separate floating skyglass blades: one central upright blade, a pair of inner diagonals, a pair of outer diagonals and two shorter flanking blades; the crystal blades outlined dark and cel shaded in two or three steps. The iron ring is split through the cyan seal stone, the two halves pushed apart; a sharp white crack of light at the break; the seven skyglass blades scatter and tumble outward. No hands, no figure. Crown constraints: no gold, no glowing strings or threads, no extra crystal debris, no jewels, no giant light halo, no radiant ghost body, no ornate armour.

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

1. STYLE: the original crew's look (rendering, palette, outline weight, outfit language and proportions); this is a different person, whose head, gear and weapons are described by the text: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_deck_warden.webp  (123206 bytes, 1221 x 1221, sha256 `805c1e99bcb1e7b3…`)

~~~text
Draw ONE image for The Ninja RPG: Foundry Warden (AI avatar). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: the original crew's look (rendering, palette, outline weight, outfit language and proportions); this is a different person, whose head, gear and weapons are described by the text. Follow each reference only for its stated role.

Subject: The Foundry Warden: a Skyglass ship's crewman who keeps the drowned foundry under the wreck's keel. Head: a dark tenugui headwrap and a cloth mask. Weapon or tool: long iron crucible tongs, a small iron ladle of molten pale cyan skyglass hanging at the belt. Stance: a lean, braced working guard, tongs held forward like a polearm. Keep: a scorched dark leather apron over an indigo kimono, sleeves tied back with a tasuki cord, soaked to the knees; not bulky, not brown overall. Rank: a regular shinobi, lean and agile; the head, the weapon or tool and the action carry his identity.

Style: Edo-era Japanese fantasy ninja, premium pixel art matching the original Skyglass crew in density and darkness: fine, deliberate pixel clusters, hard dark outlines about one art pixel wide, flat cel shading in two or three value steps per material, limited palette; no chunky retro sprite, no smoothing, no bloom, no airbrush. Colour: night-ink and deep indigo cloth, storm-grey iron, weathered leather; pale skyglass cyan only where it is materially there (eyes, a skyglass part, a chakra-worked edge); rope only for functional lashings and containers. Full body, eye level, front three-quarter view, inside the frame with a clear margin; grounded adult anatomy, readable at 125 px; both arms within the silhouette.
Costume (common crew language, not a uniform): Edo shinobi layered kimono, haori, hakama or fitted wraps; a cloth mask; a hood, headwrap or hat; an indigo waist sash; closed tabi with wrapped shins; practical arm protection; plain lacquered armour only where the subject asks for it, never ornate parade armour; torn hems and sash ends may show movement. The head described in the subject replaces these defaults. One dominant weapon or working tool. Solid gloved hands with five fingers.
He is a fully solid shinobi recalled as a chakra impression, with normal anatomy and equipment; the only signs are small chakra-lit eyes and a faint haze at the cloth's torn edges.
Chakra, if any, is compact and purposeful, at a working blade, tool or hand; no free-floating spell effects.
On a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no electronic or futuristic objects, no terminals, screens, cables, laboratory machinery or futuristic weapons, no transparent body, no floating limbs, no ghost hands, no glowing seams or veins, no crystal skin, no glitch effects, no threads or lines from the head, no gold, no filigree, no jewellery, no tassels, no crown, no ornate parade armour, no headband, no forehead protector, no clan or village symbol, no text, no bare toes, no aura or halo, no rainbow accents, no realistic or smooth painterly rendering, no anime-scaled eyes, no blur, no scenery, no floor, no cast shadow on the key colour, no key-colour spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no sheet, no grid.

Return the raw image named raw_avatar_skyglass_foundry_warden.png.
~~~

### 8. Armsmaster (commander)

References (download and attach, in this order):

1. STYLE: the original crew's look (rendering, palette, outline weight, outfit language and proportions); this is a different person, whose head, gear and weapons are described by the text: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_deck_warden.webp  (123206 bytes, 1221 x 1221, sha256 `805c1e99bcb1e7b3…`)

~~~text
Draw ONE image for The Ninja RPG: Armsmaster (commander). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: the original crew's look (rendering, palette, outline weight, outfit language and proportions); this is a different person, whose head, gear and weapons are described by the text. Follow each reference only for its stated role.

Subject: Armsmaster: Crownhold, Division I (Armoury). Head: an asymmetric, shallow, notched iron jingasa over a cloth mask. Weapon or prop: ONE broad curved short-handled ono war-axe. Stance: tall, a controlled diagonal axe strike. Keep: no second axe; no drawn spear; no back filled with weapons. Rank: a commander, about a tenth taller than a regular, NOT wider: a structured raised collar, a longer split haori, a controlled battle stance; no oversized shoulder plates, no gold, no crown. Division I, Armoury: an angular, aggressive silhouette, a short split coat, the weapon prominent. Division material: weathered forge-rust (#624C49) as a subdued, non-glowing cloth or lacquer shade on trim and panels; pale skyglass cyan stays the only luminous colour.

Style: Edo-era Japanese fantasy ninja, premium pixel art matching the original Skyglass crew in density and darkness: fine, deliberate pixel clusters, hard dark outlines about one art pixel wide, flat cel shading in two or three value steps per material, limited palette; no chunky retro sprite, no smoothing, no bloom, no airbrush. Colour: night-ink and deep indigo cloth, storm-grey iron, weathered leather; pale skyglass cyan only where it is materially there (eyes, a skyglass part, a chakra-worked edge); rope only for functional lashings and containers. Full body, eye level, front three-quarter view, inside the frame with a clear margin; grounded adult anatomy, readable at 125 px; both arms within the silhouette.
Costume (common crew language, not a uniform): Edo shinobi layered kimono, haori, hakama or fitted wraps; a cloth mask; a hood, headwrap or hat; an indigo waist sash; closed tabi with wrapped shins; practical arm protection; plain lacquered armour only where the subject asks for it, never ornate parade armour; torn hems and sash ends may show movement. The head described in the subject replaces these defaults. One dominant weapon or working tool. Solid gloved hands with five fingers.
He is a fully solid shinobi recalled as a chakra impression, with normal anatomy and equipment; the only signs are small chakra-lit eyes and a faint haze at the cloth's torn edges.
Chakra, if any, is compact and purposeful, at a working blade, tool or hand; no free-floating spell effects.
On a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no electronic or futuristic objects, no terminals, screens, cables, laboratory machinery or futuristic weapons, no transparent body, no floating limbs, no ghost hands, no glowing seams or veins, no crystal skin, no glitch effects, no threads or lines from the head, no gold, no filigree, no jewellery, no tassels, no crown, no ornate parade armour, no headband, no forehead protector, no clan or village symbol, no text, no bare toes, no aura or halo, no rainbow accents, no realistic or smooth painterly rendering, no anime-scaled eyes, no blur, no scenery, no floor, no cast shadow on the key colour, no key-colour spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no sheet, no grid.

Return the raw image named raw_avatar_crownhold_master_of_arms.png.
~~~

### 9. Replicant Zero (commander)

References (download and attach, in this order):

1. STYLE: the original crew's look (rendering, palette, outline weight, outfit language and proportions); this is a different person, whose head, gear and weapons are described by the text: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_deck_warden.webp  (123206 bytes, 1221 x 1221, sha256 `805c1e99bcb1e7b3…`)

~~~text
Draw ONE image for The Ninja RPG: Replicant Zero (commander). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: the original crew's look (rendering, palette, outline weight, outfit language and proportions); this is a different person, whose head, gear and weapons are described by the text. Follow each reference only for its stated role.

Subject: Replicant Zero: Crownhold, Division II (Research). Head: a close medical coif framed by a raised collar. Weapon or prop: hand-forged surgical forceps; a medic's scroll case at the waist. Stance: examining his own complete, solid left hand. Keep: the left hand is whole and solid; no ghost or missing hand. Rank: a commander, about a tenth taller than a regular, NOT wider: a structured raised collar, a longer split haori, a controlled battle stance; no oversized shoulder plates, no gold, no crown. Division II, Research: a narrow, vertical, asymmetric silhouette, scroll and seal equipment. Division material: muted ink-mauve (#4C444C) as a subdued, non-glowing cloth or lacquer shade on trim and panels; pale skyglass cyan stays the only luminous colour.

Style: Edo-era Japanese fantasy ninja, premium pixel art matching the original Skyglass crew in density and darkness: fine, deliberate pixel clusters, hard dark outlines about one art pixel wide, flat cel shading in two or three value steps per material, limited palette; no chunky retro sprite, no smoothing, no bloom, no airbrush. Colour: night-ink and deep indigo cloth, storm-grey iron, weathered leather; pale skyglass cyan only where it is materially there (eyes, a skyglass part, a chakra-worked edge); rope only for functional lashings and containers. Full body, eye level, front three-quarter view, inside the frame with a clear margin; grounded adult anatomy, readable at 125 px; both arms within the silhouette.
Costume (common crew language, not a uniform): Edo shinobi layered kimono, haori, hakama or fitted wraps; a cloth mask; a hood, headwrap or hat; an indigo waist sash; closed tabi with wrapped shins; practical arm protection; plain lacquered armour only where the subject asks for it, never ornate parade armour; torn hems and sash ends may show movement. The head described in the subject replaces these defaults. One dominant weapon or working tool. Solid gloved hands with five fingers.
He is a fully solid shinobi recalled as a chakra impression, with normal anatomy and equipment; the only signs are small chakra-lit eyes and a faint haze at the cloth's torn edges.
Chakra, if any, is compact and purposeful, at a working blade, tool or hand; no free-floating spell effects.
On a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no electronic or futuristic objects, no terminals, screens, cables, laboratory machinery or futuristic weapons, no transparent body, no floating limbs, no ghost hands, no glowing seams or veins, no crystal skin, no glitch effects, no threads or lines from the head, no gold, no filigree, no jewellery, no tassels, no crown, no ornate parade armour, no headband, no forehead protector, no clan or village symbol, no text, no bare toes, no aura or halo, no rainbow accents, no realistic or smooth painterly rendering, no anime-scaled eyes, no blur, no scenery, no floor, no cast shadow on the key colour, no key-colour spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no sheet, no grid.

Return the raw image named raw_avatar_crownhold_replicant_zero.png.
~~~

### 10. The Second (commander)

References (download and attach, in this order):

1. STYLE: the original crew's look (rendering, palette, outline weight, outfit language and proportions); this is a different person, whose head, gear and weapons are described by the text: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_deck_warden.webp  (123206 bytes, 1221 x 1221, sha256 `805c1e99bcb1e7b3…`)

~~~text
Draw ONE image for The Ninja RPG: The Second (commander). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: the original crew's look (rendering, palette, outline weight, outfit language and proportions); this is a different person, whose head, gear and weapons are described by the text. Follow each reference only for its stated role.

Subject: The Second: Crownhold, Division III (High Command). Head: a wide, nearly flat woven kasa over a cloth mask, a short grey beard below. Weapon or prop: an unsheathed straight shikomi-zue blade. Stance: tall and defensive, the blade low and outward. Keep: severe and composed; never hands behind the back. Rank: a commander, about a tenth taller than a regular, NOT wider: a structured raised collar, a longer split haori, a controlled battle stance; no oversized shoulder plates, no gold, no crown. Division III, High Command: a clean directional silhouette, disciplined weapon handling, restrained straight coat panels. Division material: storm-slate (#5C6474) as a subdued, non-glowing cloth or lacquer shade on trim and panels; pale skyglass cyan stays the only luminous colour.

Style: Edo-era Japanese fantasy ninja, premium pixel art matching the original Skyglass crew in density and darkness: fine, deliberate pixel clusters, hard dark outlines about one art pixel wide, flat cel shading in two or three value steps per material, limited palette; no chunky retro sprite, no smoothing, no bloom, no airbrush. Colour: night-ink and deep indigo cloth, storm-grey iron, weathered leather; pale skyglass cyan only where it is materially there (eyes, a skyglass part, a chakra-worked edge); rope only for functional lashings and containers. Full body, eye level, front three-quarter view, inside the frame with a clear margin; grounded adult anatomy, readable at 125 px; both arms within the silhouette.
Costume (common crew language, not a uniform): Edo shinobi layered kimono, haori, hakama or fitted wraps; a cloth mask; a hood, headwrap or hat; an indigo waist sash; closed tabi with wrapped shins; practical arm protection; plain lacquered armour only where the subject asks for it, never ornate parade armour; torn hems and sash ends may show movement. The head described in the subject replaces these defaults. One dominant weapon or working tool. Solid gloved hands with five fingers.
He is a fully solid shinobi recalled as a chakra impression, with normal anatomy and equipment; the only signs are small chakra-lit eyes and a faint haze at the cloth's torn edges.
Chakra, if any, is compact and purposeful, at a working blade, tool or hand; no free-floating spell effects.
On a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no electronic or futuristic objects, no terminals, screens, cables, laboratory machinery or futuristic weapons, no transparent body, no floating limbs, no ghost hands, no glowing seams or veins, no crystal skin, no glitch effects, no threads or lines from the head, no gold, no filigree, no jewellery, no tassels, no crown, no ornate parade armour, no headband, no forehead protector, no clan or village symbol, no text, no bare toes, no aura or halo, no rainbow accents, no realistic or smooth painterly rendering, no anime-scaled eyes, no blur, no scenery, no floor, no cast shadow on the key colour, no key-colour spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no sheet, no grid.

Return the raw image named raw_avatar_crownhold_the_grand_marshal.png.
~~~

### 11. Trialmaster

References (download and attach, in this order):

1. STYLE: the original crew's look (rendering, palette, outline weight, outfit language and proportions); this is a different person, whose head, gear and weapons are described by the text: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_deck_warden.webp  (123206 bytes, 1221 x 1221, sha256 `805c1e99bcb1e7b3…`)

~~~text
Draw ONE image for The Ninja RPG: Trialmaster. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: the original crew's look (rendering, palette, outline weight, outfit language and proportions); this is a different person, whose head, gear and weapons are described by the text. Follow each reference only for its stated role.

Subject: Trialmaster: Crownhold, Division I (Armoury). Head: a flat tenugui headwrap tied in a square knot at the back. Weapon or prop: a single long bokken. Stance: a two-handed intercepting sparring guard. Rank: a regular shinobi, lean and agile; the head, the weapon or tool and the action carry his identity. Division I, Armoury: an angular, aggressive silhouette, a short split coat, the weapon prominent. Division material: weathered forge-rust (#624C49) as a subdued, non-glowing cloth or lacquer shade on trim and panels; pale skyglass cyan stays the only luminous colour.

Style: Edo-era Japanese fantasy ninja, premium pixel art matching the original Skyglass crew in density and darkness: fine, deliberate pixel clusters, hard dark outlines about one art pixel wide, flat cel shading in two or three value steps per material, limited palette; no chunky retro sprite, no smoothing, no bloom, no airbrush. Colour: night-ink and deep indigo cloth, storm-grey iron, weathered leather; pale skyglass cyan only where it is materially there (eyes, a skyglass part, a chakra-worked edge); rope only for functional lashings and containers. Full body, eye level, front three-quarter view, inside the frame with a clear margin; grounded adult anatomy, readable at 125 px; both arms within the silhouette.
Costume (common crew language, not a uniform): Edo shinobi layered kimono, haori, hakama or fitted wraps; a cloth mask; a hood, headwrap or hat; an indigo waist sash; closed tabi with wrapped shins; practical arm protection; plain lacquered armour only where the subject asks for it, never ornate parade armour; torn hems and sash ends may show movement. The head described in the subject replaces these defaults. One dominant weapon or working tool. Solid gloved hands with five fingers.
He is a fully solid shinobi recalled as a chakra impression, with normal anatomy and equipment; the only signs are small chakra-lit eyes and a faint haze at the cloth's torn edges.
Chakra, if any, is compact and purposeful, at a working blade, tool or hand; no free-floating spell effects.
On a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no electronic or futuristic objects, no terminals, screens, cables, laboratory machinery or futuristic weapons, no transparent body, no floating limbs, no ghost hands, no glowing seams or veins, no crystal skin, no glitch effects, no threads or lines from the head, no gold, no filigree, no jewellery, no tassels, no crown, no ornate parade armour, no headband, no forehead protector, no clan or village symbol, no text, no bare toes, no aura or halo, no rainbow accents, no realistic or smooth painterly rendering, no anime-scaled eyes, no blur, no scenery, no floor, no cast shadow on the key colour, no key-colour spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no sheet, no grid.

Return the raw image named raw_avatar_crownhold_proving_proctor.png.
~~~

### 12. Tagwright

References (download and attach, in this order):

1. STYLE: the original crew's look (rendering, palette, outline weight, outfit language and proportions); this is a different person, whose head, gear and weapons are described by the text: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_deck_warden.webp  (123206 bytes, 1221 x 1221, sha256 `805c1e99bcb1e7b3…`)

~~~text
Draw ONE image for The Ninja RPG: Tagwright. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: the original crew's look (rendering, palette, outline weight, outfit language and proportions); this is a different person, whose head, gear and weapons are described by the text. Follow each reference only for its stated role.

Subject: Tagwright: Crownhold, Division I (Armoury). Head: a squared, short-peaked, soot-dark hood. Weapon or prop: three broad paper explosive tags held in a throwing fan. Stance: twisting forward to throw. Rank: a regular shinobi, lean and agile; the head, the weapon or tool and the action carry his identity. Division I, Armoury: an angular, aggressive silhouette, a short split coat, the weapon prominent. Division material: weathered forge-rust (#624C49) as a subdued, non-glowing cloth or lacquer shade on trim and panels; pale skyglass cyan stays the only luminous colour.

Style: Edo-era Japanese fantasy ninja, premium pixel art matching the original Skyglass crew in density and darkness: fine, deliberate pixel clusters, hard dark outlines about one art pixel wide, flat cel shading in two or three value steps per material, limited palette; no chunky retro sprite, no smoothing, no bloom, no airbrush. Colour: night-ink and deep indigo cloth, storm-grey iron, weathered leather; pale skyglass cyan only where it is materially there (eyes, a skyglass part, a chakra-worked edge); rope only for functional lashings and containers. Full body, eye level, front three-quarter view, inside the frame with a clear margin; grounded adult anatomy, readable at 125 px; both arms within the silhouette.
Costume (common crew language, not a uniform): Edo shinobi layered kimono, haori, hakama or fitted wraps; a cloth mask; a hood, headwrap or hat; an indigo waist sash; closed tabi with wrapped shins; practical arm protection; plain lacquered armour only where the subject asks for it, never ornate parade armour; torn hems and sash ends may show movement. The head described in the subject replaces these defaults. One dominant weapon or working tool. Solid gloved hands with five fingers.
He is a fully solid shinobi recalled as a chakra impression, with normal anatomy and equipment; the only signs are small chakra-lit eyes and a faint haze at the cloth's torn edges.
Chakra, if any, is compact and purposeful, at a working blade, tool or hand; no free-floating spell effects.
On a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no electronic or futuristic objects, no terminals, screens, cables, laboratory machinery or futuristic weapons, no transparent body, no floating limbs, no ghost hands, no glowing seams or veins, no crystal skin, no glitch effects, no threads or lines from the head, no gold, no filigree, no jewellery, no tassels, no crown, no ornate parade armour, no headband, no forehead protector, no clan or village symbol, no text, no bare toes, no aura or halo, no rainbow accents, no realistic or smooth painterly rendering, no anime-scaled eyes, no blur, no scenery, no floor, no cast shadow on the key colour, no key-colour spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no sheet, no grid.

Return the raw image named raw_avatar_crownhold_ordnance_quartermaster.png.
~~~

### 13. Lancer

References (download and attach, in this order):

1. STYLE: the original crew's look (rendering, palette, outline weight, outfit language and proportions); this is a different person, whose head, gear and weapons are described by the text: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_deck_warden.webp  (123206 bytes, 1221 x 1221, sha256 `805c1e99bcb1e7b3…`)

~~~text
Draw ONE image for The Ninja RPG: Lancer. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: the original crew's look (rendering, palette, outline weight, outfit language and proportions); this is a different person, whose head, gear and weapons are described by the text. Follow each reference only for its stated role.

Subject: Lancer: Crownhold, Division I (Armoury). Head: a fitted ridged cap with a short rear flap. Weapon or prop: a long fork-headed yari thrust horizontally. Stance: a committed forward lunge. Keep: not an upright spear held at rest; no crystal spearhead. Rank: a regular shinobi, lean and agile; the head, the weapon or tool and the action carry his identity. Division I, Armoury: an angular, aggressive silhouette, a short split coat, the weapon prominent. Division material: weathered forge-rust (#624C49) as a subdued, non-glowing cloth or lacquer shade on trim and panels; pale skyglass cyan stays the only luminous colour.

Style: Edo-era Japanese fantasy ninja, premium pixel art matching the original Skyglass crew in density and darkness: fine, deliberate pixel clusters, hard dark outlines about one art pixel wide, flat cel shading in two or three value steps per material, limited palette; no chunky retro sprite, no smoothing, no bloom, no airbrush. Colour: night-ink and deep indigo cloth, storm-grey iron, weathered leather; pale skyglass cyan only where it is materially there (eyes, a skyglass part, a chakra-worked edge); rope only for functional lashings and containers. Full body, eye level, front three-quarter view, inside the frame with a clear margin; grounded adult anatomy, readable at 125 px; both arms within the silhouette.
Costume (common crew language, not a uniform): Edo shinobi layered kimono, haori, hakama or fitted wraps; a cloth mask; a hood, headwrap or hat; an indigo waist sash; closed tabi with wrapped shins; practical arm protection; plain lacquered armour only where the subject asks for it, never ornate parade armour; torn hems and sash ends may show movement. The head described in the subject replaces these defaults. One dominant weapon or working tool. Solid gloved hands with five fingers.
He is a fully solid shinobi recalled as a chakra impression, with normal anatomy and equipment; the only signs are small chakra-lit eyes and a faint haze at the cloth's torn edges.
Chakra, if any, is compact and purposeful, at a working blade, tool or hand; no free-floating spell effects.
On a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no electronic or futuristic objects, no terminals, screens, cables, laboratory machinery or futuristic weapons, no transparent body, no floating limbs, no ghost hands, no glowing seams or veins, no crystal skin, no glitch effects, no threads or lines from the head, no gold, no filigree, no jewellery, no tassels, no crown, no ornate parade armour, no headband, no forehead protector, no clan or village symbol, no text, no bare toes, no aura or halo, no rainbow accents, no realistic or smooth painterly rendering, no anime-scaled eyes, no blur, no scenery, no floor, no cast shadow on the key colour, no key-colour spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no sheet, no grid.

Return the raw image named raw_avatar_crownhold_prototype_lancer_unit.png.
~~~

### 14. Duelist

References (download and attach, in this order):

1. STYLE: the original crew's look (rendering, palette, outline weight, outfit language and proportions); this is a different person, whose head, gear and weapons are described by the text: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_deck_warden.webp  (123206 bytes, 1221 x 1221, sha256 `805c1e99bcb1e7b3…`)

~~~text
Draw ONE image for The Ninja RPG: Duelist. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: the original crew's look (rendering, palette, outline weight, outfit language and proportions); this is a different person, whose head, gear and weapons are described by the text. Follow each reference only for its stated role.

Subject: Duelist: Crownhold, Division I (Armoury). Head: a diagonally tied tenugui with one rear cloth fold. Weapon or prop: a slim single drawn tachi. Stance: a long one-handed fencing cut. Rank: a regular shinobi, lean and agile; the head, the weapon or tool and the action carry his identity. Division I, Armoury: an angular, aggressive silhouette, a short split coat, the weapon prominent. Division material: weathered forge-rust (#624C49) as a subdued, non-glowing cloth or lacquer shade on trim and panels; pale skyglass cyan stays the only luminous colour.

Style: Edo-era Japanese fantasy ninja, premium pixel art matching the original Skyglass crew in density and darkness: fine, deliberate pixel clusters, hard dark outlines about one art pixel wide, flat cel shading in two or three value steps per material, limited palette; no chunky retro sprite, no smoothing, no bloom, no airbrush. Colour: night-ink and deep indigo cloth, storm-grey iron, weathered leather; pale skyglass cyan only where it is materially there (eyes, a skyglass part, a chakra-worked edge); rope only for functional lashings and containers. Full body, eye level, front three-quarter view, inside the frame with a clear margin; grounded adult anatomy, readable at 125 px; both arms within the silhouette.
Costume (common crew language, not a uniform): Edo shinobi layered kimono, haori, hakama or fitted wraps; a cloth mask; a hood, headwrap or hat; an indigo waist sash; closed tabi with wrapped shins; practical arm protection; plain lacquered armour only where the subject asks for it, never ornate parade armour; torn hems and sash ends may show movement. The head described in the subject replaces these defaults. One dominant weapon or working tool. Solid gloved hands with five fingers.
He is a fully solid shinobi recalled as a chakra impression, with normal anatomy and equipment; the only signs are small chakra-lit eyes and a faint haze at the cloth's torn edges.
Chakra, if any, is compact and purposeful, at a working blade, tool or hand; no free-floating spell effects.
On a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no electronic or futuristic objects, no terminals, screens, cables, laboratory machinery or futuristic weapons, no transparent body, no floating limbs, no ghost hands, no glowing seams or veins, no crystal skin, no glitch effects, no threads or lines from the head, no gold, no filigree, no jewellery, no tassels, no crown, no ornate parade armour, no headband, no forehead protector, no clan or village symbol, no text, no bare toes, no aura or halo, no rainbow accents, no realistic or smooth painterly rendering, no anime-scaled eyes, no blur, no scenery, no floor, no cast shadow on the key colour, no key-colour spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no sheet, no grid.

Return the raw image named raw_avatar_crownhold_calibration_duelist.png.
~~~

### 15. Archivist

References (download and attach, in this order):

1. STYLE: the original crew's look (rendering, palette, outline weight, outfit language and proportions); this is a different person, whose head, gear and weapons are described by the text: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_deck_warden.webp  (123206 bytes, 1221 x 1221, sha256 `805c1e99bcb1e7b3…`)

~~~text
Draw ONE image for The Ninja RPG: Archivist. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: the original crew's look (rendering, palette, outline weight, outfit language and proportions); this is a different person, whose head, gear and weapons are described by the text. Follow each reference only for its stated role.

Subject: Archivist: Crownhold, Division II (Research). Head: a compact, square-folded cloth eboshi. Weapon or prop: an open V-shaped bound ledger. Stance: a guarded sideways stance, ink-stained gloves. Rank: a regular shinobi, lean and agile; the head, the weapon or tool and the action carry his identity. Division II, Research: a narrow, vertical, asymmetric silhouette, scroll and seal equipment. Division material: muted ink-mauve (#4C444C) as a subdued, non-glowing cloth or lacquer shade on trim and panels; pale skyglass cyan stays the only luminous colour.

Style: Edo-era Japanese fantasy ninja, premium pixel art matching the original Skyglass crew in density and darkness: fine, deliberate pixel clusters, hard dark outlines about one art pixel wide, flat cel shading in two or three value steps per material, limited palette; no chunky retro sprite, no smoothing, no bloom, no airbrush. Colour: night-ink and deep indigo cloth, storm-grey iron, weathered leather; pale skyglass cyan only where it is materially there (eyes, a skyglass part, a chakra-worked edge); rope only for functional lashings and containers. Full body, eye level, front three-quarter view, inside the frame with a clear margin; grounded adult anatomy, readable at 125 px; both arms within the silhouette.
Costume (common crew language, not a uniform): Edo shinobi layered kimono, haori, hakama or fitted wraps; a cloth mask; a hood, headwrap or hat; an indigo waist sash; closed tabi with wrapped shins; practical arm protection; plain lacquered armour only where the subject asks for it, never ornate parade armour; torn hems and sash ends may show movement. The head described in the subject replaces these defaults. One dominant weapon or working tool. Solid gloved hands with five fingers.
He is a fully solid shinobi recalled as a chakra impression, with normal anatomy and equipment; the only signs are small chakra-lit eyes and a faint haze at the cloth's torn edges.
Chakra, if any, is compact and purposeful, at a working blade, tool or hand; no free-floating spell effects.
On a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no electronic or futuristic objects, no terminals, screens, cables, laboratory machinery or futuristic weapons, no transparent body, no floating limbs, no ghost hands, no glowing seams or veins, no crystal skin, no glitch effects, no threads or lines from the head, no gold, no filigree, no jewellery, no tassels, no crown, no ornate parade armour, no headband, no forehead protector, no clan or village symbol, no text, no bare toes, no aura or halo, no rainbow accents, no realistic or smooth painterly rendering, no anime-scaled eyes, no blur, no scenery, no floor, no cast shadow on the key colour, no key-colour spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no sheet, no grid.

Return the raw image named raw_avatar_crownhold_skyglass_archive_keeper.png.
~~~

### 16. Binder

References (download and attach, in this order):

1. STYLE: the original crew's look (rendering, palette, outline weight, outfit language and proportions); this is a different person, whose head, gear and weapons are described by the text: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_deck_warden.webp  (123206 bytes, 1221 x 1221, sha256 `805c1e99bcb1e7b3…`)

~~~text
Draw ONE image for The Ninja RPG: Binder. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: the original crew's look (rendering, palette, outline weight, outfit language and proportions); this is a different person, whose head, gear and weapons are described by the text. Follow each reference only for its stated role.

Subject: Binder: Crownhold, Division II (Research). Head: a deep asymmetric hood with a long folded side panel. Weapon or prop: a large three-toothed iron sealing key. Stance: a low, deliberate sealing guard. Rank: a regular shinobi, lean and agile; the head, the weapon or tool and the action carry his identity. Division II, Research: a narrow, vertical, asymmetric silhouette, scroll and seal equipment. Division material: muted ink-mauve (#4C444C) as a subdued, non-glowing cloth or lacquer shade on trim and panels; pale skyglass cyan stays the only luminous colour.

Style: Edo-era Japanese fantasy ninja, premium pixel art matching the original Skyglass crew in density and darkness: fine, deliberate pixel clusters, hard dark outlines about one art pixel wide, flat cel shading in two or three value steps per material, limited palette; no chunky retro sprite, no smoothing, no bloom, no airbrush. Colour: night-ink and deep indigo cloth, storm-grey iron, weathered leather; pale skyglass cyan only where it is materially there (eyes, a skyglass part, a chakra-worked edge); rope only for functional lashings and containers. Full body, eye level, front three-quarter view, inside the frame with a clear margin; grounded adult anatomy, readable at 125 px; both arms within the silhouette.
Costume (common crew language, not a uniform): Edo shinobi layered kimono, haori, hakama or fitted wraps; a cloth mask; a hood, headwrap or hat; an indigo waist sash; closed tabi with wrapped shins; practical arm protection; plain lacquered armour only where the subject asks for it, never ornate parade armour; torn hems and sash ends may show movement. The head described in the subject replaces these defaults. One dominant weapon or working tool. Solid gloved hands with five fingers.
He is a fully solid shinobi recalled as a chakra impression, with normal anatomy and equipment; the only signs are small chakra-lit eyes and a faint haze at the cloth's torn edges.
Chakra, if any, is compact and purposeful, at a working blade, tool or hand; no free-floating spell effects.
On a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no electronic or futuristic objects, no terminals, screens, cables, laboratory machinery or futuristic weapons, no transparent body, no floating limbs, no ghost hands, no glowing seams or veins, no crystal skin, no glitch effects, no threads or lines from the head, no gold, no filigree, no jewellery, no tassels, no crown, no ornate parade armour, no headband, no forehead protector, no clan or village symbol, no text, no bare toes, no aura or halo, no rainbow accents, no realistic or smooth painterly rendering, no anime-scaled eyes, no blur, no scenery, no floor, no cast shadow on the key colour, no key-colour spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no sheet, no grid.

Return the raw image named raw_avatar_crownhold_impression_containment_warden.png.
~~~

### 17. Echo

References (download and attach, in this order):

1. STYLE: the original crew's look (rendering, palette, outline weight, outfit language and proportions); this is a different person, whose head, gear and weapons are described by the text: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_deck_warden.webp  (123206 bytes, 1221 x 1221, sha256 `805c1e99bcb1e7b3…`)

~~~text
Draw ONE image for The Ninja RPG: Echo. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: the original crew's look (rendering, palette, outline weight, outfit language and proportions); this is a different person, whose head, gear and weapons are described by the text. Follow each reference only for its stated role.

Subject: Echo: Crownhold, Division II (Research). Head: a split-topped hood with two unequal peaks. Weapon or prop: a single three-pronged iron sai. Stance: an off-centre, twisted stance. Keep: one solid figure only; the instability shows only as haze at the cloth edges; no clone, no double image, no glitch. Rank: a regular shinobi, lean and agile; the head, the weapon or tool and the action carry his identity. Division II, Research: a narrow, vertical, asymmetric silhouette, scroll and seal equipment. Division material: muted ink-mauve (#4C444C) as a subdued, non-glowing cloth or lacquer shade on trim and panels; pale skyglass cyan stays the only luminous colour.

Style: Edo-era Japanese fantasy ninja, premium pixel art matching the original Skyglass crew in density and darkness: fine, deliberate pixel clusters, hard dark outlines about one art pixel wide, flat cel shading in two or three value steps per material, limited palette; no chunky retro sprite, no smoothing, no bloom, no airbrush. Colour: night-ink and deep indigo cloth, storm-grey iron, weathered leather; pale skyglass cyan only where it is materially there (eyes, a skyglass part, a chakra-worked edge); rope only for functional lashings and containers. Full body, eye level, front three-quarter view, inside the frame with a clear margin; grounded adult anatomy, readable at 125 px; both arms within the silhouette.
Costume (common crew language, not a uniform): Edo shinobi layered kimono, haori, hakama or fitted wraps; a cloth mask; a hood, headwrap or hat; an indigo waist sash; closed tabi with wrapped shins; practical arm protection; plain lacquered armour only where the subject asks for it, never ornate parade armour; torn hems and sash ends may show movement. The head described in the subject replaces these defaults. One dominant weapon or working tool. Solid gloved hands with five fingers.
He is a fully solid shinobi recalled as a chakra impression, with normal anatomy and equipment; the only signs are small chakra-lit eyes and a faint haze at the cloth's torn edges.
Chakra, if any, is compact and purposeful, at a working blade, tool or hand; no free-floating spell effects.
On a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no electronic or futuristic objects, no terminals, screens, cables, laboratory machinery or futuristic weapons, no transparent body, no floating limbs, no ghost hands, no glowing seams or veins, no crystal skin, no glitch effects, no threads or lines from the head, no gold, no filigree, no jewellery, no tassels, no crown, no ornate parade armour, no headband, no forehead protector, no clan or village symbol, no text, no bare toes, no aura or halo, no rainbow accents, no realistic or smooth painterly rendering, no anime-scaled eyes, no blur, no scenery, no floor, no cast shadow on the key colour, no key-colour spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no sheet, no grid.

Return the raw image named raw_avatar_crownhold_unstable_echo_subject.png.
~~~

### 18. Stonebound

References (download and attach, in this order):

1. STYLE: the original crew's look (rendering, palette, outline weight, outfit language and proportions); this is a different person, whose head, gear and weapons are described by the text: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_deck_warden.webp  (123206 bytes, 1221 x 1221, sha256 `805c1e99bcb1e7b3…`)

~~~text
Draw ONE image for The Ninja RPG: Stonebound. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: the original crew's look (rendering, palette, outline weight, outfit language and proportions); this is a different person, whose head, gear and weapons are described by the text. Follow each reference only for its stated role.

Subject: Stonebound: Crownhold, Division II (Research). Head: a sloping brow-wrap with one rough earth plate. Weapon or prop: a short spiked iron tetsubo. Stance: a grounded, guarded stance. Keep: compact earth armour on one arm and shoulder only; not a bulky rock golem. Rank: a regular shinobi, lean and agile; the head, the weapon or tool and the action carry his identity. Division II, Research: a narrow, vertical, asymmetric silhouette, scroll and seal equipment. Division material: muted ink-mauve (#4C444C) as a subdued, non-glowing cloth or lacquer shade on trim and panels; pale skyglass cyan stays the only luminous colour.

Style: Edo-era Japanese fantasy ninja, premium pixel art matching the original Skyglass crew in density and darkness: fine, deliberate pixel clusters, hard dark outlines about one art pixel wide, flat cel shading in two or three value steps per material, limited palette; no chunky retro sprite, no smoothing, no bloom, no airbrush. Colour: night-ink and deep indigo cloth, storm-grey iron, weathered leather; pale skyglass cyan only where it is materially there (eyes, a skyglass part, a chakra-worked edge); rope only for functional lashings and containers. Full body, eye level, front three-quarter view, inside the frame with a clear margin; grounded adult anatomy, readable at 125 px; both arms within the silhouette.
Costume (common crew language, not a uniform): Edo shinobi layered kimono, haori, hakama or fitted wraps; a cloth mask; a hood, headwrap or hat; an indigo waist sash; closed tabi with wrapped shins; practical arm protection; plain lacquered armour only where the subject asks for it, never ornate parade armour; torn hems and sash ends may show movement. The head described in the subject replaces these defaults. One dominant weapon or working tool. Solid gloved hands with five fingers.
He is a fully solid shinobi recalled as a chakra impression, with normal anatomy and equipment; the only signs are small chakra-lit eyes and a faint haze at the cloth's torn edges.
Chakra, if any, is compact and purposeful, at a working blade, tool or hand; no free-floating spell effects.
On a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no electronic or futuristic objects, no terminals, screens, cables, laboratory machinery or futuristic weapons, no transparent body, no floating limbs, no ghost hands, no glowing seams or veins, no crystal skin, no glitch effects, no threads or lines from the head, no gold, no filigree, no jewellery, no tassels, no crown, no ornate parade armour, no headband, no forehead protector, no clan or village symbol, no text, no bare toes, no aura or halo, no rainbow accents, no realistic or smooth painterly rendering, no anime-scaled eyes, no blur, no scenery, no floor, no cast shadow on the key colour, no key-colour spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no sheet, no grid.

Return the raw image named raw_avatar_crownhold_failed_reconstruction_prototype.png.
~~~

### 19. Signaller

References (download and attach, in this order):

1. STYLE: the original crew's look (rendering, palette, outline weight, outfit language and proportions); this is a different person, whose head, gear and weapons are described by the text: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_deck_warden.webp  (123206 bytes, 1221 x 1221, sha256 `805c1e99bcb1e7b3…`)

~~~text
Draw ONE image for The Ninja RPG: Signaller. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: the original crew's look (rendering, palette, outline weight, outfit language and proportions); this is a different person, whose head, gear and weapons are described by the text. Follow each reference only for its stated role.

Subject: Signaller: Crownhold, Division III (High Command). Head: a side-folded hood with a triangular ear flap. Weapon or prop: a large oval gunbai war fan; a small nobori flag on the back. Stance: directing a troop movement with an extended arm. Rank: a regular shinobi, lean and agile; the head, the weapon or tool and the action carry his identity. Division III, High Command: a clean directional silhouette, disciplined weapon handling, restrained straight coat panels. Division material: storm-slate (#5C6474) as a subdued, non-glowing cloth or lacquer shade on trim and panels; pale skyglass cyan stays the only luminous colour.

Style: Edo-era Japanese fantasy ninja, premium pixel art matching the original Skyglass crew in density and darkness: fine, deliberate pixel clusters, hard dark outlines about one art pixel wide, flat cel shading in two or three value steps per material, limited palette; no chunky retro sprite, no smoothing, no bloom, no airbrush. Colour: night-ink and deep indigo cloth, storm-grey iron, weathered leather; pale skyglass cyan only where it is materially there (eyes, a skyglass part, a chakra-worked edge); rope only for functional lashings and containers. Full body, eye level, front three-quarter view, inside the frame with a clear margin; grounded adult anatomy, readable at 125 px; both arms within the silhouette.
Costume (common crew language, not a uniform): Edo shinobi layered kimono, haori, hakama or fitted wraps; a cloth mask; a hood, headwrap or hat; an indigo waist sash; closed tabi with wrapped shins; practical arm protection; plain lacquered armour only where the subject asks for it, never ornate parade armour; torn hems and sash ends may show movement. The head described in the subject replaces these defaults. One dominant weapon or working tool. Solid gloved hands with five fingers.
He is a fully solid shinobi recalled as a chakra impression, with normal anatomy and equipment; the only signs are small chakra-lit eyes and a faint haze at the cloth's torn edges.
Chakra, if any, is compact and purposeful, at a working blade, tool or hand; no free-floating spell effects.
On a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no electronic or futuristic objects, no terminals, screens, cables, laboratory machinery or futuristic weapons, no transparent body, no floating limbs, no ghost hands, no glowing seams or veins, no crystal skin, no glitch effects, no threads or lines from the head, no gold, no filigree, no jewellery, no tassels, no crown, no ornate parade armour, no headband, no forehead protector, no clan or village symbol, no text, no bare toes, no aura or halo, no rainbow accents, no realistic or smooth painterly rendering, no anime-scaled eyes, no blur, no scenery, no floor, no cast shadow on the key colour, no key-colour spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no sheet, no grid.

Return the raw image named raw_avatar_crownhold_command_signal_adjutant.png.
~~~

### 20. Tactician

References (download and attach, in this order):

1. STYLE: the original crew's look (rendering, palette, outline weight, outfit language and proportions); this is a different person, whose head, gear and weapons are described by the text: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_deck_warden.webp  (123206 bytes, 1221 x 1221, sha256 `805c1e99bcb1e7b3…`)

~~~text
Draw ONE image for The Ninja RPG: Tactician. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: the original crew's look (rendering, palette, outline weight, outfit language and proportions); this is a different person, whose head, gear and weapons are described by the text. Follow each reference only for its stated role.

Subject: Tactician: Crownhold, Division III (High Command). Head: a narrow, tall, three-fold angled cloth cap. Weapon or prop: a black-iron jitte with its side prong visible; a small campaign map case at the waist. Stance: a guarded, pointer-like fighting stance. Rank: a regular shinobi, lean and agile; the head, the weapon or tool and the action carry his identity. Division III, High Command: a clean directional silhouette, disciplined weapon handling, restrained straight coat panels. Division material: storm-slate (#5C6474) as a subdued, non-glowing cloth or lacquer shade on trim and panels; pale skyglass cyan stays the only luminous colour.

Style: Edo-era Japanese fantasy ninja, premium pixel art matching the original Skyglass crew in density and darkness: fine, deliberate pixel clusters, hard dark outlines about one art pixel wide, flat cel shading in two or three value steps per material, limited palette; no chunky retro sprite, no smoothing, no bloom, no airbrush. Colour: night-ink and deep indigo cloth, storm-grey iron, weathered leather; pale skyglass cyan only where it is materially there (eyes, a skyglass part, a chakra-worked edge); rope only for functional lashings and containers. Full body, eye level, front three-quarter view, inside the frame with a clear margin; grounded adult anatomy, readable at 125 px; both arms within the silhouette.
Costume (common crew language, not a uniform): Edo shinobi layered kimono, haori, hakama or fitted wraps; a cloth mask; a hood, headwrap or hat; an indigo waist sash; closed tabi with wrapped shins; practical arm protection; plain lacquered armour only where the subject asks for it, never ornate parade armour; torn hems and sash ends may show movement. The head described in the subject replaces these defaults. One dominant weapon or working tool. Solid gloved hands with five fingers.
He is a fully solid shinobi recalled as a chakra impression, with normal anatomy and equipment; the only signs are small chakra-lit eyes and a faint haze at the cloth's torn edges.
Chakra, if any, is compact and purposeful, at a working blade, tool or hand; no free-floating spell effects.
On a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no electronic or futuristic objects, no terminals, screens, cables, laboratory machinery or futuristic weapons, no transparent body, no floating limbs, no ghost hands, no glowing seams or veins, no crystal skin, no glitch effects, no threads or lines from the head, no gold, no filigree, no jewellery, no tassels, no crown, no ornate parade armour, no headband, no forehead protector, no clan or village symbol, no text, no bare toes, no aura or halo, no rainbow accents, no realistic or smooth painterly rendering, no anime-scaled eyes, no blur, no scenery, no floor, no cast shadow on the key colour, no key-colour spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no sheet, no grid.

Return the raw image named raw_avatar_crownhold_high_command_staff_tactician.png.
~~~

### 21. Honor Guard

References (download and attach, in this order):

1. STYLE: the original crew's look (rendering, palette, outline weight, outfit language and proportions); this is a different person, whose head, gear and weapons are described by the text: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_deck_warden.webp  (123206 bytes, 1221 x 1221, sha256 `805c1e99bcb1e7b3…`)

~~~text
Draw ONE image for The Ninja RPG: Honor Guard. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: the original crew's look (rendering, palette, outline weight, outfit language and proportions); this is a different person, whose head, gear and weapons are described by the text. Follow each reference only for its stated role.

Subject: Honor Guard: Crownhold, Division III (High Command). Head: a fitted hood beneath a triangular iron brow visor. Weapon or prop: a long broad-bladed naginata. Stance: a controlled diagonal sweeping guard. Keep: not ornate ceremonial samurai armour. Rank: a regular shinobi, lean and agile; the head, the weapon or tool and the action carry his identity. Division III, High Command: a clean directional silhouette, disciplined weapon handling, restrained straight coat panels. Division material: storm-slate (#5C6474) as a subdued, non-glowing cloth or lacquer shade on trim and panels; pale skyglass cyan stays the only luminous colour.

Style: Edo-era Japanese fantasy ninja, premium pixel art matching the original Skyglass crew in density and darkness: fine, deliberate pixel clusters, hard dark outlines about one art pixel wide, flat cel shading in two or three value steps per material, limited palette; no chunky retro sprite, no smoothing, no bloom, no airbrush. Colour: night-ink and deep indigo cloth, storm-grey iron, weathered leather; pale skyglass cyan only where it is materially there (eyes, a skyglass part, a chakra-worked edge); rope only for functional lashings and containers. Full body, eye level, front three-quarter view, inside the frame with a clear margin; grounded adult anatomy, readable at 125 px; both arms within the silhouette.
Costume (common crew language, not a uniform): Edo shinobi layered kimono, haori, hakama or fitted wraps; a cloth mask; a hood, headwrap or hat; an indigo waist sash; closed tabi with wrapped shins; practical arm protection; plain lacquered armour only where the subject asks for it, never ornate parade armour; torn hems and sash ends may show movement. The head described in the subject replaces these defaults. One dominant weapon or working tool. Solid gloved hands with five fingers.
He is a fully solid shinobi recalled as a chakra impression, with normal anatomy and equipment; the only signs are small chakra-lit eyes and a faint haze at the cloth's torn edges.
Chakra, if any, is compact and purposeful, at a working blade, tool or hand; no free-floating spell effects.
On a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no electronic or futuristic objects, no terminals, screens, cables, laboratory machinery or futuristic weapons, no transparent body, no floating limbs, no ghost hands, no glowing seams or veins, no crystal skin, no glitch effects, no threads or lines from the head, no gold, no filigree, no jewellery, no tassels, no crown, no ornate parade armour, no headband, no forehead protector, no clan or village symbol, no text, no bare toes, no aura or halo, no rainbow accents, no realistic or smooth painterly rendering, no anime-scaled eyes, no blur, no scenery, no floor, no cast shadow on the key colour, no key-colour spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no sheet, no grid.

Return the raw image named raw_avatar_crownhold_honor_guard_commandant.png.
~~~

### 22. Runner

References (download and attach, in this order):

1. STYLE: the original crew's look (rendering, palette, outline weight, outfit language and proportions); this is a different person, whose head, gear and weapons are described by the text: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_deck_warden.webp  (123206 bytes, 1221 x 1221, sha256 `805c1e99bcb1e7b3…`)

~~~text
Draw ONE image for The Ninja RPG: Runner. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: the original crew's look (rendering, palette, outline weight, outfit language and proportions); this is a different person, whose head, gear and weapons are described by the text. Follow each reference only for its stated role.

Subject: Runner: Crownhold, Division III (High Command). Head: a tight wrap with two short ties streaming behind. Weapon or prop: a single iron kunai held forward; two bamboo dispatch tubes high on the back. Stance: a low, rapid running strike. Rank: a regular shinobi, lean and agile; the head, the weapon or tool and the action carry his identity. Division III, High Command: a clean directional silhouette, disciplined weapon handling, restrained straight coat panels. Division material: storm-slate (#5C6474) as a subdued, non-glowing cloth or lacquer shade on trim and panels; pale skyglass cyan stays the only luminous colour.

Style: Edo-era Japanese fantasy ninja, premium pixel art matching the original Skyglass crew in density and darkness: fine, deliberate pixel clusters, hard dark outlines about one art pixel wide, flat cel shading in two or three value steps per material, limited palette; no chunky retro sprite, no smoothing, no bloom, no airbrush. Colour: night-ink and deep indigo cloth, storm-grey iron, weathered leather; pale skyglass cyan only where it is materially there (eyes, a skyglass part, a chakra-worked edge); rope only for functional lashings and containers. Full body, eye level, front three-quarter view, inside the frame with a clear margin; grounded adult anatomy, readable at 125 px; both arms within the silhouette.
Costume (common crew language, not a uniform): Edo shinobi layered kimono, haori, hakama or fitted wraps; a cloth mask; a hood, headwrap or hat; an indigo waist sash; closed tabi with wrapped shins; practical arm protection; plain lacquered armour only where the subject asks for it, never ornate parade armour; torn hems and sash ends may show movement. The head described in the subject replaces these defaults. One dominant weapon or working tool. Solid gloved hands with five fingers.
He is a fully solid shinobi recalled as a chakra impression, with normal anatomy and equipment; the only signs are small chakra-lit eyes and a faint haze at the cloth's torn edges.
Chakra, if any, is compact and purposeful, at a working blade, tool or hand; no free-floating spell effects.
On a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no electronic or futuristic objects, no terminals, screens, cables, laboratory machinery or futuristic weapons, no transparent body, no floating limbs, no ghost hands, no glowing seams or veins, no crystal skin, no glitch effects, no threads or lines from the head, no gold, no filigree, no jewellery, no tassels, no crown, no ornate parade armour, no headband, no forehead protector, no clan or village symbol, no text, no bare toes, no aura or halo, no rainbow accents, no realistic or smooth painterly rendering, no anime-scaled eyes, no blur, no scenery, no floor, no cast shadow on the key colour, no key-colour spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no sheet, no grid.

Return the raw image named raw_avatar_crownhold_strategists_aide_de_camp.png.
~~~

### 23. Vanguard

References (download and attach, in this order):

1. STYLE: the original crew's look (rendering, palette, outline weight, outfit language and proportions); this is a different person, whose head, gear and weapons are described by the text: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_deck_warden.webp  (123206 bytes, 1221 x 1221, sha256 `805c1e99bcb1e7b3…`)

~~~text
Draw ONE image for The Ninja RPG: Vanguard. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: the original crew's look (rendering, palette, outline weight, outfit language and proportions); this is a different person, whose head, gear and weapons are described by the text. Follow each reference only for its stated role.

Subject: Vanguard: Crownhold, Division IV (Sanctum). Head: a low angular iron fighting hood with a notched brow. Weapon or prop: a short-handled iron fire-hook. Stance: an advancing assault. Keep: a few contained ember pixels at the hook only; no fiery body aura. Rank: a regular shinobi, lean and agile; the head, the weapon or tool and the action carry his identity. Division IV, Sanctum: a severe enclosed silhouette, the darkest clothing, straight seal panels, almost no accessories. Division material: pale iron-ash (#86858A) as a subdued, non-glowing cloth or lacquer shade on trim and panels; pale skyglass cyan stays the only luminous colour.

Style: Edo-era Japanese fantasy ninja, premium pixel art matching the original Skyglass crew in density and darkness: fine, deliberate pixel clusters, hard dark outlines about one art pixel wide, flat cel shading in two or three value steps per material, limited palette; no chunky retro sprite, no smoothing, no bloom, no airbrush. Colour: night-ink and deep indigo cloth, storm-grey iron, weathered leather; pale skyglass cyan only where it is materially there (eyes, a skyglass part, a chakra-worked edge); rope only for functional lashings and containers. Full body, eye level, front three-quarter view, inside the frame with a clear margin; grounded adult anatomy, readable at 125 px; both arms within the silhouette.
Costume (common crew language, not a uniform): Edo shinobi layered kimono, haori, hakama or fitted wraps; a cloth mask; a hood, headwrap or hat; an indigo waist sash; closed tabi with wrapped shins; practical arm protection; plain lacquered armour only where the subject asks for it, never ornate parade armour; torn hems and sash ends may show movement. The head described in the subject replaces these defaults. One dominant weapon or working tool. Solid gloved hands with five fingers.
He is a fully solid shinobi recalled as a chakra impression, with normal anatomy and equipment; the only signs are small chakra-lit eyes and a faint haze at the cloth's torn edges.
Chakra, if any, is compact and purposeful, at a working blade, tool or hand; no free-floating spell effects.
On a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no electronic or futuristic objects, no terminals, screens, cables, laboratory machinery or futuristic weapons, no transparent body, no floating limbs, no ghost hands, no glowing seams or veins, no crystal skin, no glitch effects, no threads or lines from the head, no gold, no filigree, no jewellery, no tassels, no crown, no ornate parade armour, no headband, no forehead protector, no clan or village symbol, no text, no bare toes, no aura or halo, no rainbow accents, no realistic or smooth painterly rendering, no anime-scaled eyes, no blur, no scenery, no floor, no cast shadow on the key colour, no key-colour spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no sheet, no grid.

Return the raw image named raw_avatar_crownhold_sanctum_vanguard.png.
~~~

### 24. Herald

References (download and attach, in this order):

1. STYLE: the original crew's look (rendering, palette, outline weight, outfit language and proportions); this is a different person, whose head, gear and weapons are described by the text: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_deck_warden.webp  (123206 bytes, 1221 x 1221, sha256 `805c1e99bcb1e7b3…`)

~~~text
Draw ONE image for The Ninja RPG: Herald. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: the original crew's look (rendering, palette, outline weight, outfit language and proportions); this is a different person, whose head, gear and weapons are described by the text. Follow each reference only for its stated role.

Subject: Herald: Crownhold, Division IV (Sanctum). Head: a tall, forward-bent cloth eboshi. Weapon or prop: a vertical decree scroll in one hand and a short tanto in the other. Stance: delivering an order while battle-ready. Keep: no floating text; no illuminated parchment panels. Rank: a regular shinobi, lean and agile; the head, the weapon or tool and the action carry his identity. Division IV, Sanctum: a severe enclosed silhouette, the darkest clothing, straight seal panels, almost no accessories. Division material: pale iron-ash (#86858A) as a subdued, non-glowing cloth or lacquer shade on trim and panels; pale skyglass cyan stays the only luminous colour.

Style: Edo-era Japanese fantasy ninja, premium pixel art matching the original Skyglass crew in density and darkness: fine, deliberate pixel clusters, hard dark outlines about one art pixel wide, flat cel shading in two or three value steps per material, limited palette; no chunky retro sprite, no smoothing, no bloom, no airbrush. Colour: night-ink and deep indigo cloth, storm-grey iron, weathered leather; pale skyglass cyan only where it is materially there (eyes, a skyglass part, a chakra-worked edge); rope only for functional lashings and containers. Full body, eye level, front three-quarter view, inside the frame with a clear margin; grounded adult anatomy, readable at 125 px; both arms within the silhouette.
Costume (common crew language, not a uniform): Edo shinobi layered kimono, haori, hakama or fitted wraps; a cloth mask; a hood, headwrap or hat; an indigo waist sash; closed tabi with wrapped shins; practical arm protection; plain lacquered armour only where the subject asks for it, never ornate parade armour; torn hems and sash ends may show movement. The head described in the subject replaces these defaults. One dominant weapon or working tool. Solid gloved hands with five fingers.
He is a fully solid shinobi recalled as a chakra impression, with normal anatomy and equipment; the only signs are small chakra-lit eyes and a faint haze at the cloth's torn edges.
Chakra, if any, is compact and purposeful, at a working blade, tool or hand; no free-floating spell effects.
On a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no electronic or futuristic objects, no terminals, screens, cables, laboratory machinery or futuristic weapons, no transparent body, no floating limbs, no ghost hands, no glowing seams or veins, no crystal skin, no glitch effects, no threads or lines from the head, no gold, no filigree, no jewellery, no tassels, no crown, no ornate parade armour, no headband, no forehead protector, no clan or village symbol, no text, no bare toes, no aura or halo, no rainbow accents, no realistic or smooth painterly rendering, no anime-scaled eyes, no blur, no scenery, no floor, no cast shadow on the key colour, no key-colour spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no sheet, no grid.

Return the raw image named raw_avatar_crownhold_directive_herald.png.
~~~

### 25. Last Watch

References (download and attach, in this order):

1. STYLE: the original crew's look (rendering, palette, outline weight, outfit language and proportions); this is a different person, whose head, gear and weapons are described by the text: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_deck_warden.webp  (123206 bytes, 1221 x 1221, sha256 `805c1e99bcb1e7b3…`)

~~~text
Draw ONE image for The Ninja RPG: Last Watch. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: the original crew's look (rendering, palette, outline weight, outfit language and proportions); this is a different person, whose head, gear and weapons are described by the text. Follow each reference only for its stated role.

Subject: Last Watch: Crownhold, Division IV (Sanctum). Head: a deep crescent night hood with uneven corners. Weapon or prop: ONE kusarigama with a physical short chain and weight. Stance: a low predatory stance, one controlled chain arc. Keep: no enormous supernatural chain loops. Rank: a regular shinobi, lean and agile; the head, the weapon or tool and the action carry his identity. Division IV, Sanctum: a severe enclosed silhouette, the darkest clothing, straight seal panels, almost no accessories. Division material: pale iron-ash (#86858A) as a subdued, non-glowing cloth or lacquer shade on trim and panels; pale skyglass cyan stays the only luminous colour.

Style: Edo-era Japanese fantasy ninja, premium pixel art matching the original Skyglass crew in density and darkness: fine, deliberate pixel clusters, hard dark outlines about one art pixel wide, flat cel shading in two or three value steps per material, limited palette; no chunky retro sprite, no smoothing, no bloom, no airbrush. Colour: night-ink and deep indigo cloth, storm-grey iron, weathered leather; pale skyglass cyan only where it is materially there (eyes, a skyglass part, a chakra-worked edge); rope only for functional lashings and containers. Full body, eye level, front three-quarter view, inside the frame with a clear margin; grounded adult anatomy, readable at 125 px; both arms within the silhouette.
Costume (common crew language, not a uniform): Edo shinobi layered kimono, haori, hakama or fitted wraps; a cloth mask; a hood, headwrap or hat; an indigo waist sash; closed tabi with wrapped shins; practical arm protection; plain lacquered armour only where the subject asks for it, never ornate parade armour; torn hems and sash ends may show movement. The head described in the subject replaces these defaults. One dominant weapon or working tool. Solid gloved hands with five fingers.
He is a fully solid shinobi recalled as a chakra impression, with normal anatomy and equipment; the only signs are small chakra-lit eyes and a faint haze at the cloth's torn edges.
Chakra, if any, is compact and purposeful, at a working blade, tool or hand; no free-floating spell effects.
On a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no electronic or futuristic objects, no terminals, screens, cables, laboratory machinery or futuristic weapons, no transparent body, no floating limbs, no ghost hands, no glowing seams or veins, no crystal skin, no glitch effects, no threads or lines from the head, no gold, no filigree, no jewellery, no tassels, no crown, no ornate parade armour, no headband, no forehead protector, no clan or village symbol, no text, no bare toes, no aura or halo, no rainbow accents, no realistic or smooth painterly rendering, no anime-scaled eyes, no blur, no scenery, no floor, no cast shadow on the key colour, no key-colour spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no sheet, no grid.

Return the raw image named raw_avatar_crownhold_last_watch_executor.png.
~~~

### 26. Sealbearer

References (download and attach, in this order):

1. STYLE: the original crew's look (rendering, palette, outline weight, outfit language and proportions); this is a different person, whose head, gear and weapons are described by the text: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_deck_warden.webp  (123206 bytes, 1221 x 1221, sha256 `805c1e99bcb1e7b3…`)

~~~text
Draw ONE image for The Ninja RPG: Sealbearer. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: the original crew's look (rendering, palette, outline weight, outfit language and proportions); this is a different person, whose head, gear and weapons are described by the text. Follow each reference only for its stated role.

Subject: Sealbearer: Crownhold, Division IV (Sanctum). Head: a rigid box-shaped cowl with a rectangular brow tab. Weapon or prop: an upright rectangular blackwood command-seal tablet. Stance: holding the tablet forward, the other hand ready to seal. Keep: the tablet carries the Skyglass emblem, a four-point star in a diamond, as its only seal; no screen-like glow. Rank: a regular shinobi, lean and agile; the head, the weapon or tool and the action carry his identity. Division IV, Sanctum: a severe enclosed silhouette, the darkest clothing, straight seal panels, almost no accessories. Division material: pale iron-ash (#86858A) as a subdued, non-glowing cloth or lacquer shade on trim and panels; pale skyglass cyan stays the only luminous colour.

Style: Edo-era Japanese fantasy ninja, premium pixel art matching the original Skyglass crew in density and darkness: fine, deliberate pixel clusters, hard dark outlines about one art pixel wide, flat cel shading in two or three value steps per material, limited palette; no chunky retro sprite, no smoothing, no bloom, no airbrush. Colour: night-ink and deep indigo cloth, storm-grey iron, weathered leather; pale skyglass cyan only where it is materially there (eyes, a skyglass part, a chakra-worked edge); rope only for functional lashings and containers. Full body, eye level, front three-quarter view, inside the frame with a clear margin; grounded adult anatomy, readable at 125 px; both arms within the silhouette.
Costume (common crew language, not a uniform): Edo shinobi layered kimono, haori, hakama or fitted wraps; a cloth mask; a hood, headwrap or hat; an indigo waist sash; closed tabi with wrapped shins; practical arm protection; plain lacquered armour only where the subject asks for it, never ornate parade armour; torn hems and sash ends may show movement. The head described in the subject replaces these defaults. One dominant weapon or working tool. Solid gloved hands with five fingers.
He is a fully solid shinobi recalled as a chakra impression, with normal anatomy and equipment; the only signs are small chakra-lit eyes and a faint haze at the cloth's torn edges.
Chakra, if any, is compact and purposeful, at a working blade, tool or hand; no free-floating spell effects.
On a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no electronic or futuristic objects, no terminals, screens, cables, laboratory machinery or futuristic weapons, no transparent body, no floating limbs, no ghost hands, no glowing seams or veins, no crystal skin, no glitch effects, no threads or lines from the head, no gold, no filigree, no jewellery, no tassels, no crown, no ornate parade armour, no headband, no forehead protector, no clan or village symbol, no text, no bare toes, no aura or halo, no rainbow accents, no realistic or smooth painterly rendering, no anime-scaled eyes, no blur, no scenery, no floor, no cast shadow on the key colour, no key-colour spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no sheet, no grid.

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

Subject: Inside the castle armoury: long wooden racks of yari, naginata and katana, a straw-target trial range on packed earth, a wooden placard by the first rack, cold stone walls and worn tatami. (Used by: Division I opening, the Trialmaster.)

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

Subject: An open ordnance store past the trial range: a wooden counter with a ledger, lacquered boxes of paper explosive tags glowing faintly at their edges, scorch marks on the stone. (Used by: the Tagwright.)

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

Subject: A narrow stone spear-trial gallery: a heavy wooden thrusting post bound in iron bands and scorched by lightning chakra, split straw targets along the walls, a few crackling sparks. (Used by: the Lancer.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_crownhold_test_gallery.png.
~~~

### 31. Scene: Armory command shrine

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp  (250006 bytes, 1536 x 1024, sha256 `babd22ccf728fb67…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp  (85260 bytes, 728 x 728, sha256 `60087ce9e1d64019…`)

~~~text
Draw ONE image for The Ninja RPG: Scene: Armory command shrine. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: A carved command shrine set into the armoury wall beside a sealed door: a lacquered seal desk with a glowing skyglass seal stone, and a low crawlway hatch behind the weapon racks closed by a three-bolt wooden lock. (Used by: Division I command node, puzzle, protocols.)

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

Subject: The armoury's heart: a towering forge wall hung with every weapon type ever tested, a glowing charcoal forge, an anvil, a sealed door behind. (Used by: the Armsmaster.)

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

Subject: An archive hall of tall wooden shelves: paper-tagged boxes of skyglass record crystals, each holding a faint sleeping light, and racks of scrolls; cold blue air, a low reading desk with an open ledger. (Used by: Division II opening, the Archivist.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_crownhold_archive_of_impressions.png.
~~~

### 34. Scene: Sealing jar halls

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp  (250006 bytes, 1536 x 1024, sha256 `babd22ccf728fb67…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp  (85260 bytes, 728 x 728, sha256 `60087ce9e1d64019…`)

~~~text
Draw ONE image for The Ninja RPG: Scene: Sealing jar halls. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: Halls of tall sealed ceramic jars and lacquered wooden tubs bound in rope and paper seals, a few glowing faintly from within, lit by one tall skyglass lantern pillar; iron rings of seal keys on hooks; one jar cracked and dark. (Used by: the Binder, the Echo.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_crownhold_vat_halls.png.
~~~

### 35. Scene: Research command shrine

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp  (250006 bytes, 1536 x 1024, sha256 `babd22ccf728fb67…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp  (85260 bytes, 728 x 728, sha256 `60087ce9e1d64019…`)

~~~text
Draw ONE image for The Ninja RPG: Scene: Research command shrine. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: A carved command seal desk beside the sliding door of the recall chamber, a wooden plaque on the door, a locked stair behind the sealing jars. (Used by: Division II command node, puzzle, protocols.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_crownhold_research_terminal.png.
~~~

### 36. Scene: Recall chamber

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp  (250006 bytes, 1536 x 1024, sha256 `babd22ccf728fb67…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp  (85260 bytes, 728 x 728, sha256 `60087ce9e1d64019…`)

~~~text
Draw ONE image for The Ninja RPG: Scene: Recall chamber. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: A recall chamber seen from a raised wooden gallery behind half-open shoji panels: a central tatami floor ringed by low tiered benches, an empty healer's table under a frame of bamboo and paper seals with skyglass crystals hung on cords. (Used by: Replicant Zero.)

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

Subject: A signal tower room: a long wooden board of signal bells and coloured cords, a taiko drum by the window, a scroll on the writing desk filling with brushed lines one by one as if an unseen hand writes, maps of borders that no longer exist on the walls; empty of people. (Used by: Division III opening, the Signaller, and the aftermath; whoever sends the order is NEVER shown.)

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

Subject: A planning hall set for a war council no one will attend: a long table with campaign maps, empty chairs, an inkwell of glowing chakra ink. (Used by: the Tactician.)

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

Subject: A long corridor lined with suits of plain lacquered armour on wooden stands, naginata racked between them, leading to a closed sliding door. (Used by: the Honor Guard.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_crownhold_honor_guard_corridor.png.
~~~

### 40. Scene: High Command shrine

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp  (250006 bytes, 1536 x 1024, sha256 `babd22ccf728fb67…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp  (85260 bytes, 728 x 728, sha256 `60087ce9e1d64019…`)

~~~text
Draw ONE image for The Ninja RPG: Scene: High Command shrine. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: A carved command seal desk outside a senior officer's sliding door, a narrow service corridor beside it, bamboo dispatch tubes on a rack. (Used by: Division III command node, puzzle, protocols.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_crownhold_high_command_terminal.png.
~~~

### 41. Scene: The Second's office

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp  (250006 bytes, 1536 x 1024, sha256 `babd22ccf728fb67…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp  (85260 bytes, 728 x 728, sha256 `60087ce9e1d64019…`)

~~~text
Draw ONE image for The Ninja RPG: Scene: The Second's office. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: A severe, unadorned office: a low folding map table, a single cushion, a window onto snow, thirty years of annotated orders pinned to the wall. (Used by: the Second.)

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

Subject: The summit: a gate of dark obsidian lit by ember light at the top of a long stair, ember braziers, the Supreme Command banner. (Used by: Division IV opening, the Vanguard.)

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

Subject: An obsidian antechamber with a lectern for a herald's scroll, lightning-blue light on black stone, ember lamps. (Used by: the Herald.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_crownhold_antechamber.png.
~~~

### 44. Scene: Outer ring and shrine

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp  (250006 bytes, 1536 x 1024, sha256 `babd22ccf728fb67…`)
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp  (85260 bytes, 728 x 728, sha256 `60087ce9e1d64019…`)

~~~text
Draw ONE image for The Ninja RPG: Scene: Outer ring and shrine. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: The curved night-watch corridor of the Sanctum's outer ring, the last command shrine glowing in a wall niche, a sealed door ahead, a narrow drainage channel under an iron grate in the floor. (Used by: the Last Watch, Division IV command node, puzzle, protocols.)

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

Subject: An obsidian throne room lit by ember light, a tall summit window looking out over a whole mountain range at night, an empty command seat; seven faint blade-shaped cyan glints hang in the dark above it (the commander is not shown). (Used by: Supreme Commander Arakane.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_crownhold_throne_room.png.
~~~

### 46. The Last Directive (jutsu icon)

> BLOCKED until brief A (the Arakane v2 avatar) is approved and committed; then rerun the builder and the approved avatar joins this image as its SUBJECT reference. Do not generate before that.

References (download and attach, in this order):

1. STYLE: jutsu icon register: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/style_refs/jutsu_icons/bbe/icon_bbe_sapphire_command_v2.webp  (61270 bytes, 256 x 256, sha256 `410b8c5a20af40b2…`)

~~~text
Draw ONE image for The Ninja RPG: The Last Directive (jutsu icon). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: jutsu icon register. Follow each reference only for its stated role.

Subject: The Last Directive: a commander's final order to himself. The Command Crown's seven skyglass blades standing in a guarding circle around a single upright blade planted point-down, the blackened-iron ring and its cyan seal stone beneath. The Command Crown: a thin CLOSED ring of blackened iron with seven blunt iron seal notches and one small faceted pale cyan seal stone at the front; above it, with a small gap, seven separate floating skyglass blades: one central upright blade, a pair of inner diagonals, a pair of outer diagonals and two shorter flanking blades; the crystal blades outlined dark and cel shaded in two or three steps. No gold, no strings or threads.

Style: PREMIUM PIXEL ART jutsu icon (crisp hard-edged pixels, clean dark outlines, flat cel shading, limited palette, no painterly blur), laid out like the attached exemplar: a single bold technique emblem on a designed dark background with the same framing, rendering and detail density; square 1024 x 1024; readable at 125 px. A designed background is allowed (no chroma key needed).
Negative: no text, no letters, no UI, no watermark, no character portrait, no second emblem.

Return the raw image named raw_icon-jutsu-the-last-directive.png.
~~~

### 47. Extermination Order (jutsu icon)

> BLOCKED until brief A (the Arakane v2 avatar) is approved and committed; then rerun the builder and the approved avatar joins this image as its SUBJECT reference. Do not generate before that.

References (download and attach, in this order):

1. STYLE: jutsu icon register: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/style_refs/jutsu_icons/bbe/icon_bbe_sapphire_command_v2.webp  (61270 bytes, 256 x 256, sha256 `410b8c5a20af40b2…`)

~~~text
Draw ONE image for The Ninja RPG: Extermination Order (jutsu icon). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: jutsu icon register. Follow each reference only for its stated role.

Subject: Extermination Order: a killing command. The Command Crown's seven skyglass blades flying in from the edges and converging on one point, where a sealed elemental sigil cracks apart. No gold, no strings or threads.

Style: PREMIUM PIXEL ART jutsu icon (crisp hard-edged pixels, clean dark outlines, flat cel shading, limited palette, no painterly blur), laid out like the attached exemplar: a single bold technique emblem on a designed dark background with the same framing, rendering and detail density; square 1024 x 1024; readable at 125 px. A designed background is allowed (no chroma key needed).
Negative: no text, no letters, no UI, no watermark, no character portrait, no second emblem.

Return the raw image named raw_icon-jutsu-extermination-order.png.
~~~

### 48. Countermand (item icon)

> BLOCKED until brief A (the Arakane v2 avatar) is approved and committed; then rerun the builder and the approved avatar joins this image as its SUBJECT reference. Do not generate before that.

References (download and attach, in this order):

1. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (an object of the same crew): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_seal_charge.webp  (153182 bytes, 1174 x 1174, sha256 `6f56d9c84465f970…`)

~~~text
Draw ONE image for The Ninja RPG: Countermand (item icon). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (an object of the same crew). Follow each reference only for its stated role.

Subject: Countermand: Crownhold's command seal. A rectangular blackwood tablet framed in blackened iron, hanging on a short chain, its face carved with the Skyglass emblem, a four-point star in a diamond, and set with a small faceted pale cyan seal stone. No gold.

Style: PREMIUM PIXEL ART game item icon, the same pixel rendering as the PIXEL STYLE reference: crisp hard-edged pixels, clean dark outlines, flat cel shading with a few deliberate highlight steps, limited palette, no anti-aliased blur, no painterly gradients. Colours as the subject: cool blue-black wood and blue-grey iron, silver-grey metal highlights, ONE accent of pale cyan faceted skyglass with a small glow, cool cyan rim light. Camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no second object, no question mark, no painted or smooth illustration look, no blur.

Return the raw image named raw_icon-countermand.png.
~~~

### 49. Skyglass Coffer (pixel redraw)

References (download and attach, in this order):

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/skyglass_event_icons/exports/icon-skyglass-coffer.webp  (70574 bytes, 256 x 256, sha256 `a7bbfe7e60570aef…`)
2. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (an object of the same crew): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_seal_charge.webp  (153182 bytes, 1174 x 1174, sha256 `6f56d9c84465f970…`)

~~~text
Draw ONE image for The Ninja RPG: Skyglass Coffer (pixel redraw). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. SUBJECT: redraw this exact icon; 2. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (an object of the same crew). Follow each reference only for its stated role.

Subject: Skyglass Coffer: redraw the SUBJECT reference almost exactly (same object, shape, proportions, details, colours and accent) as premium pixel art, so it matches the rest of the set. Change nothing about the design.

Style: PREMIUM PIXEL ART game item icon, the same pixel rendering as the PIXEL STYLE reference: crisp hard-edged pixels, clean dark outlines, flat cel shading with a few deliberate highlight steps, limited palette, no anti-aliased blur, no painterly gradients. Colours exactly as the SUBJECT reference. Camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no second object, no question mark, no painted or smooth illustration look, no blur.

Return the raw image named raw_icon-skyglass-coffer-pixel.png.
~~~

### 50. Katon Tool Pouch (pixel redraw)

References (download and attach, in this order):

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/skyglass_event_icons/exports/icon-tool-pouch-katon.webp  (67920 bytes, 256 x 256, sha256 `b1fa26ced2204d1e…`)
2. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (an object of the same crew): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_seal_charge.webp  (153182 bytes, 1174 x 1174, sha256 `6f56d9c84465f970…`)

~~~text
Draw ONE image for The Ninja RPG: Katon Tool Pouch (pixel redraw). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. SUBJECT: redraw this exact icon; 2. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (an object of the same crew). Follow each reference only for its stated role.

Subject: Katon Tool Pouch: redraw the SUBJECT reference almost exactly (same object, shape, proportions, details, colours and accent) as premium pixel art, so it matches the rest of the set. Change nothing about the design.

Style: PREMIUM PIXEL ART game item icon, the same pixel rendering as the PIXEL STYLE reference: crisp hard-edged pixels, clean dark outlines, flat cel shading with a few deliberate highlight steps, limited palette, no anti-aliased blur, no painterly gradients. Colours exactly as the SUBJECT reference. Camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no second object, no question mark, no painted or smooth illustration look, no blur.

Return the raw image named raw_icon-tool-pouch-katon-pixel.png.
~~~

### 51. Wave Tool Pouch (pixel redraw)

References (download and attach, in this order):

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/skyglass_event_icons/exports/icon-tool-pouch-wave.webp  (67620 bytes, 256 x 256, sha256 `44fa5437a835a3e0…`)
2. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (an object of the same crew): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_seal_charge.webp  (153182 bytes, 1174 x 1174, sha256 `6f56d9c84465f970…`)

~~~text
Draw ONE image for The Ninja RPG: Wave Tool Pouch (pixel redraw). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. SUBJECT: redraw this exact icon; 2. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (an object of the same crew). Follow each reference only for its stated role.

Subject: Wave Tool Pouch: redraw the SUBJECT reference almost exactly (same object, shape, proportions, details, colours and accent) as premium pixel art, so it matches the rest of the set. Change nothing about the design.

Style: PREMIUM PIXEL ART game item icon, the same pixel rendering as the PIXEL STYLE reference: crisp hard-edged pixels, clean dark outlines, flat cel shading with a few deliberate highlight steps, limited palette, no anti-aliased blur, no painterly gradients. Colours exactly as the SUBJECT reference. Camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no second object, no question mark, no painted or smooth illustration look, no blur.

Return the raw image named raw_icon-tool-pouch-wave-pixel.png.
~~~

### 52. Ikazuchi Tool Pouch (pixel redraw)

References (download and attach, in this order):

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/skyglass_event_icons/exports/icon-tool-pouch-ikazuchi.webp  (68698 bytes, 256 x 256, sha256 `c644532a96cbf44e…`)
2. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (an object of the same crew): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_seal_charge.webp  (153182 bytes, 1174 x 1174, sha256 `6f56d9c84465f970…`)

~~~text
Draw ONE image for The Ninja RPG: Ikazuchi Tool Pouch (pixel redraw). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. SUBJECT: redraw this exact icon; 2. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (an object of the same crew). Follow each reference only for its stated role.

Subject: Ikazuchi Tool Pouch: redraw the SUBJECT reference almost exactly (same object, shape, proportions, details, colours and accent) as premium pixel art, so it matches the rest of the set. Change nothing about the design.

Style: PREMIUM PIXEL ART game item icon, the same pixel rendering as the PIXEL STYLE reference: crisp hard-edged pixels, clean dark outlines, flat cel shading with a few deliberate highlight steps, limited palette, no anti-aliased blur, no painterly gradients. Colours exactly as the SUBJECT reference. Camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no second object, no question mark, no painted or smooth illustration look, no blur.

Return the raw image named raw_icon-tool-pouch-ikazuchi-pixel.png.
~~~

### 53. Stonefall Tool Pouch (pixel redraw)

References (download and attach, in this order):

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/skyglass_event_icons/exports/icon-tool-pouch-stonefall.webp  (68232 bytes, 256 x 256, sha256 `029a560a5bcbc202…`)
2. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (an object of the same crew): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_seal_charge.webp  (153182 bytes, 1174 x 1174, sha256 `6f56d9c84465f970…`)

~~~text
Draw ONE image for The Ninja RPG: Stonefall Tool Pouch (pixel redraw). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. SUBJECT: redraw this exact icon; 2. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (an object of the same crew). Follow each reference only for its stated role.

Subject: Stonefall Tool Pouch: redraw the SUBJECT reference almost exactly (same object, shape, proportions, details, colours and accent) as premium pixel art, so it matches the rest of the set. Change nothing about the design.

Style: PREMIUM PIXEL ART game item icon, the same pixel rendering as the PIXEL STYLE reference: crisp hard-edged pixels, clean dark outlines, flat cel shading with a few deliberate highlight steps, limited palette, no anti-aliased blur, no painterly gradients. Colours exactly as the SUBJECT reference. Camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no second object, no question mark, no painted or smooth illustration look, no blur.

Return the raw image named raw_icon-tool-pouch-stonefall-pixel.png.
~~~

### 54. Zephyrfang Tool Pouch (pixel redraw)

References (download and attach, in this order):

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/skyglass_event_icons/exports/icon-tool-pouch-zephyrfang.webp  (66358 bytes, 256 x 256, sha256 `ca3d144715e8385b…`)
2. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (an object of the same crew): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_seal_charge.webp  (153182 bytes, 1174 x 1174, sha256 `6f56d9c84465f970…`)

~~~text
Draw ONE image for The Ninja RPG: Zephyrfang Tool Pouch (pixel redraw). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. SUBJECT: redraw this exact icon; 2. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (an object of the same crew). Follow each reference only for its stated role.

Subject: Zephyrfang Tool Pouch: redraw the SUBJECT reference almost exactly (same object, shape, proportions, details, colours and accent) as premium pixel art, so it matches the rest of the set. Change nothing about the design.

Style: PREMIUM PIXEL ART game item icon, the same pixel rendering as the PIXEL STYLE reference: crisp hard-edged pixels, clean dark outlines, flat cel shading with a few deliberate highlight steps, limited palette, no anti-aliased blur, no painterly gradients. Colours exactly as the SUBJECT reference. Camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no second object, no question mark, no painted or smooth illustration look, no blur.

Return the raw image named raw_icon-tool-pouch-zephyrfang-pixel.png.
~~~

### 55. Chart of the Drowned Foundry (pixel redraw)

References (download and attach, in this order):

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/skyglass_event_icons/exports/icon-chart-drowned-foundry.webp  (60940 bytes, 256 x 256, sha256 `0b00806939bd375a…`)
2. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (an object of the same crew): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_seal_charge.webp  (153182 bytes, 1174 x 1174, sha256 `6f56d9c84465f970…`)

~~~text
Draw ONE image for The Ninja RPG: Chart of the Drowned Foundry (pixel redraw). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. SUBJECT: redraw this exact icon; 2. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (an object of the same crew). Follow each reference only for its stated role.

Subject: Chart of the Drowned Foundry: redraw the SUBJECT reference almost exactly (same object, shape, proportions, details, colours and accent) as premium pixel art, so it matches the rest of the set. Change nothing about the design.

Style: PREMIUM PIXEL ART game item icon, the same pixel rendering as the PIXEL STYLE reference: crisp hard-edged pixels, clean dark outlines, flat cel shading with a few deliberate highlight steps, limited palette, no anti-aliased blur, no painterly gradients. Colours exactly as the SUBJECT reference. Camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no second object, no question mark, no painted or smooth illustration look, no blur.

Return the raw image named raw_icon-chart-drowned-foundry-pixel.png.
~~~

### 56. Chart of the Quarantined Archive (pixel redraw)

References (download and attach, in this order):

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/skyglass_event_icons/exports/icon-chart-quarantined-archive.webp  (65754 bytes, 256 x 256, sha256 `80df641bad0135e7…`)
2. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (an object of the same crew): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_seal_charge.webp  (153182 bytes, 1174 x 1174, sha256 `6f56d9c84465f970…`)

~~~text
Draw ONE image for The Ninja RPG: Chart of the Quarantined Archive (pixel redraw). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. SUBJECT: redraw this exact icon; 2. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (an object of the same crew). Follow each reference only for its stated role.

Subject: Chart of the Quarantined Archive: redraw the SUBJECT reference almost exactly (same object, shape, proportions, details, colours and accent) as premium pixel art, so it matches the rest of the set. Change nothing about the design.

Style: PREMIUM PIXEL ART game item icon, the same pixel rendering as the PIXEL STYLE reference: crisp hard-edged pixels, clean dark outlines, flat cel shading with a few deliberate highlight steps, limited palette, no anti-aliased blur, no painterly gradients. Colours exactly as the SUBJECT reference. Camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no second object, no question mark, no painted or smooth illustration look, no blur.

Return the raw image named raw_icon-chart-quarantined-archive-pixel.png.
~~~

### 57. Chart of the Captain's Watch (pixel redraw)

References (download and attach, in this order):

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/skyglass_event_icons/exports/icon-chart-captains-watch.webp  (68722 bytes, 256 x 256, sha256 `e576a50a3f066e97…`)
2. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (an object of the same crew): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_seal_charge.webp  (153182 bytes, 1174 x 1174, sha256 `6f56d9c84465f970…`)

~~~text
Draw ONE image for The Ninja RPG: Chart of the Captain's Watch (pixel redraw). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. SUBJECT: redraw this exact icon; 2. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (an object of the same crew). Follow each reference only for its stated role.

Subject: Chart of the Captain's Watch: redraw the SUBJECT reference almost exactly (same object, shape, proportions, details, colours and accent) as premium pixel art, so it matches the rest of the set. Change nothing about the design.

Style: PREMIUM PIXEL ART game item icon, the same pixel rendering as the PIXEL STYLE reference: crisp hard-edged pixels, clean dark outlines, flat cel shading with a few deliberate highlight steps, limited palette, no anti-aliased blur, no painterly gradients. Colours exactly as the SUBJECT reference. Camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no second object, no question mark, no painted or smooth illustration look, no blur.

Return the raw image named raw_icon-chart-captains-watch-pixel.png.
~~~

### 58. Lastlight Lantern (pixel redraw)

References (download and attach, in this order):

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/skyglass_event_icons/exports/icon-skyglass-signal-beacon.webp  (45678 bytes, 256 x 256, sha256 `6b58863e0d526502…`)
2. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (an object of the same crew): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_seal_charge.webp  (153182 bytes, 1174 x 1174, sha256 `6f56d9c84465f970…`)

~~~text
Draw ONE image for The Ninja RPG: Lastlight Lantern (pixel redraw). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. SUBJECT: redraw this exact icon; 2. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (an object of the same crew). Follow each reference only for its stated role.

Subject: Lastlight Lantern: redraw the SUBJECT reference almost exactly (same object, shape, proportions, details, colours and accent) as premium pixel art, so it matches the rest of the set. Change nothing about the design.

Style: PREMIUM PIXEL ART game item icon, the same pixel rendering as the PIXEL STYLE reference: crisp hard-edged pixels, clean dark outlines, flat cel shading with a few deliberate highlight steps, limited palette, no anti-aliased blur, no painterly gradients. Colours exactly as the SUBJECT reference. Camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no second object, no question mark, no painted or smooth illustration look, no blur.

Return the raw image named raw_icon-skyglass-signal-beacon-pixel.png.
~~~

### 59. Armory Requisition (pixel redraw)

References (download and attach, in this order):

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/skyglass_event_icons/exports/icon-armory-requisition.webp  (47944 bytes, 256 x 256, sha256 `869b66de517273ad…`)
2. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (an object of the same crew): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_seal_charge.webp  (153182 bytes, 1174 x 1174, sha256 `6f56d9c84465f970…`)

~~~text
Draw ONE image for The Ninja RPG: Armory Requisition (pixel redraw). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. SUBJECT: redraw this exact icon; 2. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (an object of the same crew). Follow each reference only for its stated role.

Subject: Armory Requisition: redraw the SUBJECT reference almost exactly (same object, shape, proportions, details, colours and accent) as premium pixel art, so it matches the rest of the set. Change nothing about the design.

Style: PREMIUM PIXEL ART game item icon, the same pixel rendering as the PIXEL STYLE reference: crisp hard-edged pixels, clean dark outlines, flat cel shading with a few deliberate highlight steps, limited palette, no anti-aliased blur, no painterly gradients. Colours exactly as the SUBJECT reference. Camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no second object, no question mark, no painted or smooth illustration look, no blur.

Return the raw image named raw_icon-armory-requisition-pixel.png.
~~~

### 60. Skyglass Crown (pixel redraw)

References (download and attach, in this order):

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/icon_ghost_ship_skyglass_crown.webp  (116290 bytes, 480 x 480, sha256 `02cde28f5fedfaf3…`)
2. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (an object of the same crew): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_seal_charge.webp  (153182 bytes, 1174 x 1174, sha256 `6f56d9c84465f970…`)

~~~text
Draw ONE image for The Ninja RPG: Skyglass Crown (pixel redraw). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. SUBJECT: redraw this exact icon; 2. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (an object of the same crew). Follow each reference only for its stated role.

Subject: Skyglass Crown: redraw the SUBJECT reference almost exactly (same object, shape, proportions, details, colours and accent) as premium pixel art, so it matches the rest of the set. Change nothing about the design.

Style: PREMIUM PIXEL ART game item icon, the same pixel rendering as the PIXEL STYLE reference: crisp hard-edged pixels, clean dark outlines, flat cel shading with a few deliberate highlight steps, limited palette, no anti-aliased blur, no painterly gradients. Colours exactly as the SUBJECT reference. Camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no second object, no question mark, no painted or smooth illustration look, no blur.

Return the raw image named raw_icon_ghost_ship_skyglass_crown_pixel.png.
~~~

### 61. Skyglass Crown Fragment (pixel redraw)

References (download and attach, in this order):

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/icon_ghost_ship_skyglass_crown_fragment.webp  (107374 bytes, 480 x 480, sha256 `434872cd478550ca…`)
2. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (an object of the same crew): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_seal_charge.webp  (153182 bytes, 1174 x 1174, sha256 `6f56d9c84465f970…`)

~~~text
Draw ONE image for The Ninja RPG: Skyglass Crown Fragment (pixel redraw). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. SUBJECT: redraw this exact icon; 2. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (an object of the same crew). Follow each reference only for its stated role.

Subject: Skyglass Crown Fragment: redraw the SUBJECT reference almost exactly (same object, shape, proportions, details, colours and accent) as premium pixel art, so it matches the rest of the set. Change nothing about the design.

Style: PREMIUM PIXEL ART game item icon, the same pixel rendering as the PIXEL STYLE reference: crisp hard-edged pixels, clean dark outlines, flat cel shading with a few deliberate highlight steps, limited palette, no anti-aliased blur, no painterly gradients. Colours exactly as the SUBJECT reference. Camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no second object, no question mark, no painted or smooth illustration look, no blur.

Return the raw image named raw_icon_ghost_ship_skyglass_crown_fragment_pixel.png.
~~~

### 62. Skyglass Crystal (pixel redraw)

References (download and attach, in this order):

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/icon_ghost_ship_skyglass_crystal.webp  (103342 bytes, 480 x 480, sha256 `896543c69115e830…`)
2. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (an object of the same crew): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_seal_charge.webp  (153182 bytes, 1174 x 1174, sha256 `6f56d9c84465f970…`)

~~~text
Draw ONE image for The Ninja RPG: Skyglass Crystal (pixel redraw). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. SUBJECT: redraw this exact icon; 2. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (an object of the same crew). Follow each reference only for its stated role.

Subject: Skyglass Crystal: redraw the SUBJECT reference almost exactly (same object, shape, proportions, details, colours and accent) as premium pixel art, so it matches the rest of the set. Change nothing about the design.

Style: PREMIUM PIXEL ART game item icon, the same pixel rendering as the PIXEL STYLE reference: crisp hard-edged pixels, clean dark outlines, flat cel shading with a few deliberate highlight steps, limited palette, no anti-aliased blur, no painterly gradients. Colours exactly as the SUBJECT reference. Camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no second object, no question mark, no painted or smooth illustration look, no blur.

Return the raw image named raw_icon_ghost_ship_skyglass_crystal_pixel.png.
~~~

### 63. Skyglass Filament (pixel redraw)

References (download and attach, in this order):

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/icon_ghost_ship_skyglass_filament.webp  (129168 bytes, 480 x 480, sha256 `b165dba7e5849bcd…`)
2. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (an object of the same crew): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_seal_charge.webp  (153182 bytes, 1174 x 1174, sha256 `6f56d9c84465f970…`)

~~~text
Draw ONE image for The Ninja RPG: Skyglass Filament (pixel redraw). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. SUBJECT: redraw this exact icon; 2. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (an object of the same crew). Follow each reference only for its stated role.

Subject: Skyglass Filament: redraw the SUBJECT reference almost exactly (same object, shape, proportions, details, colours and accent) as premium pixel art, so it matches the rest of the set. Change nothing about the design.

Style: PREMIUM PIXEL ART game item icon, the same pixel rendering as the PIXEL STYLE reference: crisp hard-edged pixels, clean dark outlines, flat cel shading with a few deliberate highlight steps, limited palette, no anti-aliased blur, no painterly gradients. Colours exactly as the SUBJECT reference. Camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no second object, no question mark, no painted or smooth illustration look, no blur.

Return the raw image named raw_icon_ghost_ship_skyglass_filament_pixel.png.
~~~

### 64. Skyglass Katana (pixel redraw)

References (download and attach, in this order):

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/icon_ghost_ship_skyglass_katana.webp  (56510 bytes, 480 x 480, sha256 `f7a336ca9fc0067a…`)
2. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (an object of the same crew): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_seal_charge.webp  (153182 bytes, 1174 x 1174, sha256 `6f56d9c84465f970…`)

~~~text
Draw ONE image for The Ninja RPG: Skyglass Katana (pixel redraw). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. SUBJECT: redraw this exact icon; 2. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (an object of the same crew). Follow each reference only for its stated role.

Subject: Skyglass Katana: redraw the SUBJECT reference almost exactly (same object, shape, proportions, details, colours and accent) as premium pixel art, so it matches the rest of the set. Change nothing about the design.

Style: PREMIUM PIXEL ART game item icon, the same pixel rendering as the PIXEL STYLE reference: crisp hard-edged pixels, clean dark outlines, flat cel shading with a few deliberate highlight steps, limited palette, no anti-aliased blur, no painterly gradients. Colours exactly as the SUBJECT reference. Camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no second object, no question mark, no painted or smooth illustration look, no blur.

Return the raw image named raw_icon_ghost_ship_skyglass_katana_pixel.png.
~~~

### 65. Skyglass Serum (pixel redraw)

References (download and attach, in this order):

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/icon_ghost_ship_skyglass_serum.webp  (277032 bytes, 768 x 768, sha256 `6d83e870aa4bdbd8…`)
2. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (an object of the same crew): https://raw.githubusercontent.com/perseverance484/tnr-tools/60b792ac19ba710d724a247127eb0482d967eeaf/art/ghost_ship_skyglass/avatar_ghost_ship_seal_charge.webp  (153182 bytes, 1174 x 1174, sha256 `6f56d9c84465f970…`)

~~~text
Draw ONE image for The Ninja RPG: Skyglass Serum (pixel redraw). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. SUBJECT: redraw this exact icon; 2. PIXEL STYLE: rendering, outline weight, shading and the rope, wood and lacquered-metal materials only (an object of the same crew). Follow each reference only for its stated role.

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

Subject: A new location: The foundry's intake hall inside the wreck, half flooded: dark water at knee height, empty seal casks bobbing against the walls, bamboo-and-timber water channels and wooden sluice gates, pale cyan light glinting off the water. (Used by: Drowned Foundry d_intake, b_intake.)

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

Subject: A new location: The pour hall: rows of stone casting moulds lashed together with rope-bound seal charges, an inspector's ledger desk, knee-deep water, and an orange-white crucible glow coming up through iron floor grates from below. (Used by: Drowned Foundry d_hall, b_hall, d_gate.)

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

Subject: Use the first reference as the starting composition and colour, changed to match this brief exactly: Below the waterline inside the wreck: the hull is rebuilding itself out of timber and rope that do not belong together, half-formed frames knitting in pale cyan seal light; a ladder down to a severed seal channel pulsing with cyan light. (Used by: Quarantined Archive d_hull, b_horror, d_conduit.)

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

