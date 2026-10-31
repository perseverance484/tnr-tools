# Skyglass art register

- **Prompts:** `docs/handoffs/SKYGLASS_ART_PROMPTS.md` (one block per TO GENERATE row)
- **Direction:** `docs/handoffs/SKYGLASS_ART_REQUEST.md`; **audit:** `docs/design/SKYGLASS_ART_AUDIT.md` (RUL-2026-10-30-061)
- **Folders:** `skyglass_art_refs.zip` (built outside the repo; the folder named per row holds the files to attach)
- **Live-game requests/writes:** 0

Status values: **TO GENERATE** (a prompt block exists; no approved raw yet), **IN REPO** (finished file committed,
upload only), **DERIVED** (Claude makes it by script from an approved base), **PROCESSED** (approved raw committed and
processed to a final export; not uploaded yet), **DERIVED: DONE** (recolour exported; not uploaded yet). Update a row when its raw is approved,
processed, and uploaded; approval, processing and upload are separate facts (`ISOLATED_ART_GENERATION.md` §4).

| Code | Name | Type | Attach folder / source | Live id | Status |
|---|---|---|---|---|---|
| IC01 | Tide Chart | ICON | `01_chart_icons` | `H1s2IwtZ5JqgPEoJ55IVj` | PROCESSED (`icon-tide-chart.webp`, push/352) |
| IC02 | Watch Roster | ICON | `01_chart_icons` | `yE8TwzygWZSNoZD5x97rW` | PROCESSED (`icon-watch-roster.webp`, push/352) |
| IC03 | Reliquary Seal | ICON | `02_seal_icons` | `sVqDdYUJIxxRYbmKbbxo0` | PROCESSED (`icon-reliquary-seal.webp`, push/352) |
| IC04 | The Last Heading | ICON | `01_chart_icons` | `s1mYHuKqw2YuzIzxVwU-_` | PROCESSED (`icon-the-last-heading.webp`, push/352) |
| IC05 | Core Rot | ICON | `03_reagent_icons` | `KuqLeFB12BdB-0s5O1udk` | PROCESSED (`icon-core-rot.webp`, push/352) |
| IC06 | Ledger Page (base; = Ledger Page: The Trophy Hold) | ICON | `01_chart_icons` | `JvrytTOdR1voVCoo3fckK` | PROCESSED (`icon-ledger-page.webp`, push/352) |
| IC07 | Stores Manifest (base; = Stores Manifest: The Overgrown Stores) | ICON | `01_chart_icons` | `nLG6TK48xlyZ_t9R28QsY` | PROCESSED (`icon-stores-manifest.webp`, push/352) |
| IC08 | Skyglass Token | ICON | `04_reward_icons` | `nzCW7A-_AuYMzBs2wClnM` | PROCESSED (`art/skyglass_event_icons/exports/icon-skyglass-token.webp`) |
| VT00 | Boss variant token BASE (VT01-VT07 attach it) | ICON | `05_variant_token` | - | NOT NEEDED (VT01-VT07 delivered directly) |
| VT01 | Captain's Gunbai (variant token) | ICON | `05_variant_token` | `vltFmOTgOyqssIpNXvT37` | PROCESSED (`art/skyglass_event_icons/exports/icon-variant-token-captains-gunbai.webp`) |
| VT02 | Rotbloom (variant token) | ICON | `05_variant_token` | `-7dQs2qwokuNSAS2c3X8Q` | PROCESSED (`art/skyglass_event_icons/exports/icon-variant-token-rotbloom.webp`) |
| VT03 | Forgefists (variant token) | ICON | `05_variant_token` | `d96tj122ex6BnzhMDwy0s` | PROCESSED (`art/skyglass_event_icons/exports/icon-variant-token-forgefists.webp`) |
| VT04 | Wayfinder (variant token) | ICON | `05_variant_token` | `giSqzJqE6YdsrnOoy1KLV` | PROCESSED (`art/skyglass_event_icons/exports/icon-variant-token-wayfinder.webp`) |
| VT05 | The First Blade (variant token) | ICON | `05_variant_token` | `5rpvgpKckgmN-vXjzJpb8` | PROCESSED (`art/skyglass_event_icons/exports/icon-variant-token-the-first-blade.webp`) |
| VT06 | Sealscript (variant token) | ICON | `05_variant_token` | `3ZR700BAWr_Pd3Eqnu1c9` | PROCESSED (`art/skyglass_event_icons/exports/icon-variant-token-sealscript.webp`) |
| VT07 | Crownbreaker (variant token) | ICON | `05_variant_token` | `pqKpEqo-x6BHTjxTRUEfD` | PROCESSED (`art/skyglass_event_icons/exports/icon-variant-token-crownbreaker.webp`) |
| IC09 | The Little Horror's Jar | ICON | `04_reward_icons` | - | PROCESSED (`art/skyglass_event_icons/exports/icon-little-horrors-jar.webp`) |
| IC10 | Galley Stores | ICON | `04_reward_icons` | `D-QTnbjgTyIVc593zzdSB` | PROCESSED (`art/skyglass_event_icons/exports/icon-galley-stores.webp`) |
| IC11 | Crown's Hoard | ICON | `04_reward_icons` | - | PROCESSED (`art/skyglass_event_icons/exports/icon-crowns-hoard.webp`) |
| IC12 | Countermand | ICON | `02_seal_icons` | `W3lOjQhhIPUYPkIZmiNum` | PROCESSED (`art/skyglass_event_icons/exports/icon-countermand.webp`) |
| VS01 | Windward (variant of Aetherion) | ICON (variant) | `10_variant_aetherion` | `MXAAH-1fwPfyDJg2FnE8t` | PROCESSED (`art/skyglass_variant_skins/exports/icon-variant-windward.webp`) |
| VS02 | Riptide (variant of Thornsilver) | ICON (variant) | `11_variant_thornsilver` | `YNhKQmKUjfVIPQkGlNO41` | PROCESSED (`art/skyglass_variant_skins/exports/icon-variant-riptide.webp`) |
| VS03 | Nightreaver (variant of Night's Testament) | ICON (variant) | `12_variant_nights_testament` | `mtx4YmUu-wkKGwnOPVbYS` | PROCESSED (`art/skyglass_variant_skins/exports/icon-variant-nightreaver.webp`) |
| VS04 | Thunderwake (variant of Stormrender; was Thunderwake) | ICON (variant) | `13_variant_stormrender` | `_49jp25nHiH-v8ywlRdKH` | PROCESSED (`art/skyglass_variant_skins/exports/icon-variant-thunderwake.webp`) |
| VS05 | Anchorline (variant of Oathbinder) | ICON (variant) | `14_variant_oathbinder` | `umsYP0jL3emdVFDdU6Fcd` | PROCESSED (`art/skyglass_variant_skins/exports/icon-variant-anchorline.webp`) |
| VS06 | Starfall (variant of Ink of the Void) | ICON (variant) | `15_variant_ink_of_the_void` | `1yWEP0r3elIzyScORfot4` | PROCESSED (`art/skyglass_variant_skins/exports/icon-variant-starfall.webp`) |
| VS07 | The Unwritten Order (variant of The Unwritten) | ICON (variant) | `16_variant_the_unwritten` | `3NH-VreJl9TcqqIYiztn_` | PROCESSED (`art/skyglass_variant_skins/exports/icon-variant-the-unwritten-order.webp`) |
| VS08 | Keelstone (variant of Gaea's Embrace) | ICON (variant) | `17_variant_gaeas_embrace` | `xFyTBqje5M1_68EqRRoBu` | PROCESSED (`art/skyglass_variant_skins/exports/icon-variant-keelstone.webp`) |
| VS09 | Skyglass Kote (variant of Warden's Bracers) | ICON (variant) | `18_variant_wardens_bracers` | `_tdmHvPnvlnIMLpRnk9GC` | PROCESSED (`art/skyglass_variant_skins/exports/icon-variant-skyglass-kote.webp`) |
| VS10 | Lastlight Duskblade (variant of Eclipsed Dawnblade) | ICON (variant) | `19_variant_eclipsed_dawnblade` | `m7Xqe9cD1oB_2vCj1Zvu5` | PROCESSED (`art/skyglass_variant_skins/exports/icon-variant-lastlight-duskblade.webp`) |
| VS11 | Skysail (variant of Zephyr's Whisper) | ICON (variant) | `20_variant_zephyrs_whisper` | `kD6g1o5qJo3K9r1HeHtiH` | PROCESSED (`art/skyglass_variant_skins/exports/icon-variant-skysail.webp`) |
| VS12 | Hullbreaker (variant of Yuki's Frostbite) | ICON (variant) | `21_variant_yukis_frostbite` | `Iew4QFXyfWLPlPoMgeDrz` | PROCESSED (`art/skyglass_variant_skins/exports/icon-variant-hullbreaker.webp`) |
| VS13 | Captain's Gunbai (variant of The Unwritten) | ICON (variant) | `16_variant_the_unwritten` | `Deo6Y7dNzaPhOAiWK-4I3` | PROCESSED (`art/skyglass_variant_skins/exports/icon-variant-captains-gunbai.webp`) |
| VS14 | Rotbloom (variant of Oathbinder) | ICON (variant) | `14_variant_oathbinder` | `dkkdXbwWFOGSw1nemyK7K` | PROCESSED (`art/skyglass_variant_skins/exports/icon-variant-rotbloom.webp`) |
| VS15 | Forgefists (variant of Warden's Bracers) | ICON (variant) | `18_variant_wardens_bracers` | `3DtT9myjmYY5xNY5mv7Ew` | PROCESSED (`art/skyglass_variant_skins/exports/icon-variant-forgefists.webp`) |
| VS16 | Wayfinder (variant of Stormrender) | ICON (variant) | `13_variant_stormrender` | `hkcF8F8RZa71dcLu8im8G` | PROCESSED (`art/skyglass_variant_skins/exports/icon-variant-wayfinder.webp`) |
| VS17 | The First Blade (variant of Aetherion) | ICON (variant) | `10_variant_aetherion` | `m_CYA2H9XDF_TbMiii8PE` | PROCESSED (`art/skyglass_variant_skins/exports/icon-variant-the-first-blade.webp`) |
| VS18 | Sealscript (variant of Whispering Dawnblade) | ICON (variant) | `22_variant_whispering_dawnblade` | `trSVpt_E_BqOJS1geL_Sn` | PROCESSED (`art/skyglass_variant_skins/exports/icon-variant-sealscript.webp`) |
| VS19 | Crownbreaker (variant of Thornsilver) | ICON (variant) | `11_variant_thornsilver` | `dt6BWKCOfuB3mPLl14-CF` | PROCESSED (`art/skyglass_variant_skins/exports/icon-variant-crownbreaker.webp`) |
| JI01 | Lastlight (jutsu icon) | JUTSU_ICON | `30_jutsu_icons` | `0F-68bxOXW_LkJnXV0lwT` | PROCESSED (`art/skyglass_jutsu_icons/exports/icon-jutsu-lastlight.webp`) |
| JI02 | Little Maw (jutsu icon) | JUTSU_ICON | `30_jutsu_icons` | - | PROCESSED (`art/skyglass_jutsu_icons/exports/icon-jutsu-little-maw.webp`) |
| JI03 | The Last Directive (jutsu icon) | JUTSU_ICON | `30_jutsu_icons` | `GHFMU_DDKvBBp5BEuTeah` | PROCESSED (`art/skyglass_jutsu_icons/exports/icon-jutsu-the-last-directive.webp`) |
| JI04 | Extermination Order (jutsu icon) | JUTSU_ICON | `30_jutsu_icons` | `EqZsaqser8c2-KpVCaXk_` | PROCESSED (`art/skyglass_jutsu_icons/exports/icon-jutsu-extermination-order.webp`) |
| AN01 | cp_command: Ward of Command banner | ANIMATION | `35_fx_layers` | - | PROCESSED (`art/skyglass_boss_fx/exports/`: `anim_fx_command_banner_v1.webp`; `an_v1.json`) |
| AN02 | cc_phase_shift: shockwave flourish | ANIMATION | `35_fx_layers` | - | PROCESSED (`art/skyglass_boss_fx/exports/`: `anim_fx_phase_shift_v1.webp`; `an_v1.json`) |
| AN03 | cp_gunwale: Raise the Gunwale barrier | gameAsset STATIC or ANIMATION | `35_fx_layers` | - | PROCESSED (`art/skyglass_boss_fx/exports/`: `anim_fx_gunwale_barrier_v1.webp`, `tile_fx_gunwale_barrier_v1.webp`; `an_v1.json`) |
| AN04 | ch_enrage: The Core Rebuilds aura | ANIMATION | `35_fx_layers` | - | PROCESSED (`art/skyglass_boss_fx/exports/`: `anim_fx_core_enrage_v1.webp`; `an_v1.json`) |
| AN05 | cc_hexweave: Hexweave hit | ANIMATION | `35_fx_layers` | - | PROCESSED (`art/skyglass_boss_fx/exports/anim_fx_hexweave_v1.webp`; redrawn 2026-10-31 as an irregular snarl) |
| AN06 | Spreading Fire ember tile | gameAsset STATIC or ANIMATION loop | `35_fx_layers` | - | PROCESSED (`art/skyglass_boss_fx/exports/`: `tile_fx_spreading_fire_embers_v1.webp`, `anim_fx_spreading_fire_glint_v1.webp`, `anim_fx_spreading_fire_embers_v1.webp`; `an_v1.json`) |
| AN07 | ch_bile_spit: glob in flight | ANIMATION | `35_fx_layers` | - | PROCESSED (`art/skyglass_boss_fx/exports/`: `anim_fx_bile_glob_v1.webp`; `an_v1.json`) |
| AN08 | ch_bile_spit: splash | ANIMATION | `35_fx_layers` | - | PROCESSED (`art/skyglass_boss_fx/exports/`: `anim_fx_bile_splash_v1.webp`; `an_v1.json`) |
| AN09 | ch_undertow: water-drag streak (OPTIONAL) | ANIMATION | `35_fx_layers` | - | PROCESSED (`art/skyglass_boss_fx/exports/`: `anim_fx_undertow_v1.webp`; `an_v1.json`) |
| PT01 | The salvager (Wreck Sighted) | SCENE_CHARACTER | `25_salvager_portrait` | - | PROCESSED (`art/skyglass_scene_chars/exports/scene_char_skyglass_salvager.webp`) |
| AV01 | Tagwright (Crown Tagwright) | AI_AVATAR | `40_crew_avatars` | `1syezT0axWVQVgeOGN-LH` | PROCESSED (`art/crownhold/avatars/exports/avatar_crownhold_tagwright.webp`) |
| AV02 | Lancer (Crown Lancer) | AI_AVATAR | `40_crew_avatars` | `e5ye0RlN0fManSKdD_k-o` | PROCESSED (`art/crownhold/avatars/exports/avatar_crownhold_lancer.webp`) |
| AV03 | Honor Guard (Honor Guard) | AI_AVATAR | `40_crew_avatars` | `1orTQQ0Q9XhBvwlSZuzj5` | PROCESSED (`art/crownhold/avatars/exports/avatar_crownhold_honor-guard.webp`) |
| AV04 | Runner (Crown Runner) | AI_AVATAR | `40_crew_avatars` | `-U_-iIwhGodkqdvc4GPa6` | PROCESSED (`art/crownhold/avatars/exports/avatar_crownhold_runner.webp`) |
| AV05 | Vanguard (Crown Vanguard) | AI_AVATAR | `40_crew_avatars` | `pshn-LkaC5vIgI6EOv68I` | PROCESSED (`art/crownhold/avatars/exports/avatar_crownhold_vanguard.webp`) |
| AV06 | Herald (Crown Herald) | AI_AVATAR | `40_crew_avatars` | `Q6QjSoH6d1SabfQOLb12-` | PROCESSED (`art/crownhold/avatars/exports/avatar_crownhold_herald.webp`) |
| AV07 | Last Watch (Last Watch) | AI_AVATAR | `40_crew_avatars` | `qQn9h2FY3GUUqgaFIRAuf` | PROCESSED (`art/crownhold/avatars/exports/avatar_crownhold_last-watch.webp`) |
| AV08 | Sealbearer (Crown Sealbearer) | AI_AVATAR | `40_crew_avatars` | `09gLgh9sCtshISC0dvpka` | PROCESSED (`art/crownhold/avatars/exports/avatar_crownhold_sealbearer.webp`) |
| SC01 | Crownhold gate (scene #27) | SCENE_BACKGROUND | `50_ship_scenes` | - | PROCESSED (`art/crownhold/scenes/exports/scene_bg_crownhold_gate.webp`) |
| SC02 | Armory proving hall (Experimental Armory) (scene #28) | SCENE_BACKGROUND | `50_ship_scenes` | - | PROCESSED (`art/crownhold/scenes/exports/scene_bg_crownhold_proving_hall.webp`) |
| SC03 | Sealing-jar halls (Skyglass Research) (scene #34) | SCENE_BACKGROUND | `50_ship_scenes` | - | PROCESSED (`art/crownhold/scenes/exports/scene_bg_crownhold_vat_halls.webp`) |
| SC04 | High Command signal room (scene #37) | SCENE_BACKGROUND | `50_ship_scenes` | - | PROCESSED (`art/crownhold/scenes/exports/scene_bg_crownhold_signal_room.webp`) |
| SC05 | Planning hall (scene #38) | SCENE_BACKGROUND | `50_ship_scenes` | - | PROCESSED (`art/crownhold/scenes/exports/scene_bg_crownhold_planning_hall.webp`) |
| SC06 | Throne room (Command Sanctum) (scene #45) | SCENE_BACKGROUND | `50_ship_scenes` | - | PROCESSED (`art/crownhold/scenes/exports/scene_bg_crownhold_throne_room.webp`) |
| DR01 | Rotted Reliquary Seal | ICON (recolour) | `from IC03` | `2sGi5SZXh2UutHmM-mIMD` | DERIVED: DONE (rot-green seal, `icon-rotted-reliquary-seal.webp`, push/352) |
| DR02 | The Rotted Heading | ICON (recolour) | `from IC04` | `U2yJbBM6_N1xBBf0ez96F` | DERIVED: DONE (rot-green seal, `icon-the-rotted-heading.webp`, push/352) |
| DR03 | Ledger Page: The Bone Store | ICON (recolour) | `from IC06` | `uu6ETQimuBJ69jwr76IIi` | DERIVED: DONE (charcoal cord, `icon-ledger-page-bone-store.webp`, push/352) |
| DR04 | Ledger Page: The Snare Room | ICON (recolour) | `from IC06` | `6QgcnW0v6gZeHY474BjR0` | DERIVED: DONE (cobalt cord, `icon-ledger-page-snare-room.webp`, push/352) |
| DR05 | Stores Manifest: The Ore Vault | ICON (recolour) | `from IC07` | `9j4IErGW1gmZ-5FNjZMEQ` | DERIVED: DONE (violet cord, `icon-stores-manifest-ore-vault.webp`, push/352) |
| DR06 | Stores Manifest: The Bloom Cellar | ICON (recolour) | `from IC07` | `7Sz2ttMScKH8b10XYS12I` | DERIVED: DONE (rose cord, `icon-stores-manifest-bloom-cellar.webp`, push/352) |
| UP01 | Sealed Treasury | ICON | `art/skyglass_event_icons/exports/icon-sealed-treasury.webp` | `Ma8S90Nmbi0Xvm4u4FzJh` | IN REPO |
| UP02 | Archive Chart Case | ICON | `art/skyglass_event_icons/exports/icon-archive-chart-case.webp` | `B48dTRsoLJGKBWIUbeUoG` | IN REPO |
| UP03 | Chart of the Buried Cache | ICON | `art/skyglass_event_icons/exports/icon-chart-buried-cache.webp` | `nbLC37UzBamthKXvZsgQB` | IN REPO |
| UP04 | Unmarked Cargo | ICON | `art/skyglass_event_icons/exports/icon-unmarked-cargo.webp` | `KzITKJ5BUQRz5QuYWw-0B` | IN REPO |
| UP05 | Crownbreaker badge v2 | ICON (badge) | `art/crownhold/icon-badge-crownbreaker-v2.webp` | `7kJGzBnfO14eKRs7_7c_f` | IN REPO |
| UP06 | Foundry Warden avatar | AI_AVATAR | `art/skyglass_event_icons/avatars/avatar_skyglass_foundry_warden.webp` | - | IN REPO |
| UP07 | Crown Armsmaster avatar | AI_AVATAR | `art/crownhold/avatar_crownhold_master_of_arms.webp` | `-GKFYAZUg1eF-3VnZhDjx` | IN REPO |
| UP08 | Replicant Zero avatar | AI_AVATAR | `art/crownhold/avatar_crownhold_replicant_zero.webp` | `vjEFUJ9mb1zNTuQf4lfXv` | IN REPO |
| UP09 | The Second avatar | AI_AVATAR | `art/crownhold/avatar_crownhold_the_grand_marshal.webp` | `ZsfRoyJ55Zsay5bHNLMPv` | IN REPO |
| UP10 | Crown Trialmaster avatar | AI_AVATAR | `art/crownhold/avatar_crownhold_proving_proctor.webp` | `1iJF8VBietrfvxJd_ZhFS` | IN REPO |
| UP11 | Crown Duelist avatar | AI_AVATAR | `art/crownhold/avatar_crownhold_calibration_duelist.webp` | `B41DtMALbOTpL82thkBZu` | IN REPO |
| UP12 | Crown Archivist avatar | AI_AVATAR | `art/crownhold/avatar_crownhold_skyglass_archive_keeper.webp` | `LZiunyinw9ScK3mh9HiR2` | IN REPO |
| UP13 | Crown Binder avatar | AI_AVATAR | `art/crownhold/avatar_crownhold_impression_containment_warden.webp` | `N3E3C6MGgVYql2pTvpuGf` | IN REPO |
| UP14 | Crown Echo avatar | AI_AVATAR | `art/crownhold/avatar_crownhold_unstable_echo_subject.webp` | `0LON_CwaUuXj4EYL7BtxS` | IN REPO |
| UP15 | Crown Stonebound avatar | AI_AVATAR | `art/crownhold/avatar_crownhold_failed_reconstruction_prototype.webp` | `jqxu13kNHhfNY-NF68Ftb` | IN REPO |
| UP16 | Crown Signaller avatar | AI_AVATAR | `art/crownhold/avatar_crownhold_command_signal_adjutant.webp` | `IJNhy83uB5Lc3sqn6Iqcr` | IN REPO |
| UP17 | Crown Tactician avatar | AI_AVATAR | `art/crownhold/avatar_crownhold_high_command_staff_tactician.webp` | `5U0WgIrowP6HdP5DrrxBS` | IN REPO |
| UP18 | anim_maw_v1 | ANIMATION | `art/skyglass_boss_fx/exports/anim_maw_v1.webp` | - | IN REPO |
| UP19 | anim_maw_field_v1 | ANIMATION | `art/skyglass_boss_fx/exports/anim_maw_field_v1.webp` | - | IN REPO |
| UP20 | anim_quench_v1 | ANIMATION | `art/skyglass_boss_fx/exports/anim_quench_v1.webp` | - | IN REPO |
| UP21 | anim_command_absolute_v1 | ANIMATION | `art/skyglass_boss_fx/exports/anim_command_absolute_v1.webp` | - | IN REPO |
| UP22 | anim_command_absolute_field_v1 | ANIMATION | `art/skyglass_boss_fx/exports/anim_command_absolute_field_v1.webp` | - | IN REPO |
| UP23 | anim_crownfall_v1 | ANIMATION | `art/skyglass_boss_fx/exports/anim_crownfall_v1.webp` | - | IN REPO |
| UP24 | anim_broadside_v1 | ANIMATION | `art/skyglass_boss_fx/exports/anim_broadside_v1.webp` | - | IN REPO |
| UP25 | anim_broadside_field_v1 | ANIMATION | `art/skyglass_boss_fx/exports/anim_broadside_field_v1.webp` | - | IN REPO |
| UP26 | anim_ships_bell_v1 | ANIMATION | `art/skyglass_boss_fx/exports/anim_ships_bell_v1.webp` | - | IN REPO |
| UP27 | anim_crimson_strike_v1 | ANIMATION | `art/skyglass_boss_fx/exports/anim_crimson_strike_v1.webp` | - | IN REPO |
| UP28 | anim_chain_wrap_v1 | ANIMATION | `art/skyglass_boss_fx/exports/anim_chain_wrap_v1.webp` | - | IN REPO |
| UP29 | anim_recall_v1 | ANIMATION | `art/skyglass_boss_fx/exports/anim_recall_v1.webp` | - | IN REPO |
| UP30 | anim_crown_aura_v1 | ANIMATION | `art/skyglass_boss_fx/exports/anim_crown_aura_v1.webp` | - | IN REPO |
| UP31 | anim_rot_claw_v1 | ANIMATION | `art/skyglass_boss_fx/exports/anim_rot_claw_v1.webp` | - | IN REPO |
| UP32 | anim_exposed_v1 | ANIMATION | `art/skyglass_boss_fx/exports/anim_exposed_v1.webp` | - | IN REPO |

**Totals:** TO GENERATE 26 · PROCESSED 41 · DERIVED: DONE 6 · IN REPO 32 · 105 rows (recounted 2026-10-31 at the AN intake).

AN01-AN09 intake 2026-10-31: raws `art/skyglass_boss_fx/raw/an/AN0n_raw_fx_*.png` (native alpha, unchanged), built by
`art/skyglass_boss_fx/animate_an.py` (drawn on the 50 px combat grid, delivered as 150 px frames, x3 nearest, to meet the
ANIMATION target's 112 px minimum; 50 ms per frame). Frames, speed and suggested use per file: `art/skyglass_boss_fx/exports/an_v1.json`;
previews `docs/design/skyglass_boss_fx/an_v1_*.png`. artpreflight `--type ANIMATION` 0/0 over 10 strips, `--type STATIC`
0/0 over 2 stills. Not uploaded; no push generator or manifest touched.

IC01-IC07 intake 2026-10-31: raws `art/skyglass_event_icons/raw/IC0n_raw_*.png` (unchanged originals; hashes in
`art/skyglass_event_icons/_provenance/`), processed and recoloured by `state/skyglass_art/ic01_07_intake.py`
(256 px lossless webp under `art/skyglass_event_icons/exports/`); upload by push/352 (`push/skyglass_chart_icons.gen.py`).

## Haul chests (PC01-PC08; new hidden items created by push/370, RUL-2026-10-31-081)

Iron = Common, bronze = Rare, silver = Epic; Legendary not yet generated. Intake 2026-10-31:
`state/skyglass_art/profession_chests_intake.py` (raws `art/skyglass_event_icons/raw/PC0n_raw_*.png`, unchanged; PC01 and
PC05 came flattened on black, so their outline is rebuilt after a border flood), artpreflight `--type ICON` 0/0 over 6 files.
push/370 picks each image up once its export exists; the two Legendary chests ship with the engine default until PC07/PC08 arrive.

| Code | Asset | Type | Folder | Live id | Status |
|---|---|---|---|---|---|
| PC01 | Hide Bundle | ICON | (director-generated) | `KwgjMOya2XT6uYsgXbsh6` | PROCESSED (`icon-common-hunters-chest.webp`, push/370) |
| PC02 | Stores Bundle | ICON | (director-generated) | `gb6vxdzWTYZR--7s-4kTX` | PROCESSED (`icon-common-gatherers-chest.webp`, push/370) |
| PC03 | Keeper's Pack | ICON | (director-generated) | `M-0CPw9yBmmreLvJU6gav` | PROCESSED (`icon-rare-hunters-chest.webp`, push/370) |
| PC04 | Quartermaster's Pack | ICON | (director-generated) | see design_data.json | PROCESSED (`icon-rare-gatherers-chest.webp`, push/370) |
| PC05 | Prize Strongbox | ICON | (director-generated) | `32k2rXF6W-7gn_Fubp4kU` | PROCESSED (`icon-epic-hunters-chest.webp`, push/370) |
| PC06 | Overgrown Strongbox | ICON | (director-generated) | see design_data.json | PROCESSED (`icon-epic-gatherers-chest.webp`, push/370) |
| PC07 | Keeper's Reserve | ICON | (director-generated) | see design_data.json | PROCESSED (`art/skyglass_event_icons/exports/icon-legendary-hunters-chest.webp`) |
| PC08 | Quartermaster's Reserve | ICON | (director-generated) | see design_data.json | PROCESSED (`art/skyglass_event_icons/exports/icon-legendary-gatherers-chest.webp`) |

FX frame size (director 2026-10-31): AN01-AN09 strips keep 150 px frames (drawn on the 50 px grid, delivered 3x) per the ANIMATION spec's 112 px minimum.
