# Skyglass event: visual asset audit

**Status:** AUDIT (Lane B planning document, 2026-10-30, `main` at `0e791fb0`). Zero live requests. It lists every visual
asset the Skyglass event (the Wreck, the chart runs, the hunts, The Haul, Crownhold, the rewards) needs, with its status,
so the director can plan art sessions. This file owns no rule. Where it disagrees with the rulings or the design docs,
they win and this file is corrected.

**Sources, latest wins:** `docs/RULINGS.md` RUL-2026-10-28-009 … RUL-2026-10-29-058 (with RUL-2026-10-25-*, -26-* and
-28-001 … -008 where they still govern art); the 2026-10-30 director decisions in `push/README.md` 326-327; every
`docs/design/SKYGLASS_*.md` (loot tables incl. the RUL-058 header and §5d, The Haul, Pets, Boss Fights, Boss Animations,
Wreck Encounters, Hunts Content, Dungeon and Treasure Hunts, Story Bible, Text incl. its §5 art lines and §9 questions);
`state/skyglass_art/items.json` and `docs/handoffs/SKYGLASS_CROWNHOLD_ART_BATCH.md` (the 79-image batch);
`state/skyglass_fx/asset_ids.json`; `state/skyglass_hunts/hunts.py`; `state/crownhold/ids.json`; the Skyglass/Crownhold
generators in `push/`; the spent manifests that created the live records (`archive/spent-manifests/push-2026-10-25/`
260-274, `push-2026-10-28/320`); the harvests in `harvests/inbox/`; the harness specs on `fable/skyglass-*-sim`; the
pet, variant and badge builder branches; `skills/producing-tnr-art/` (SKILL.md, `data/25x_DATA_art_spec.json`).

## How status was decided

| Status | Meaning | Evidence used |
|---|---|---|
| **EXISTS LIVE** | the image is uploaded and on the live record | (1) the Forge idmap (filename → uploaded URL), unioned across all 353 result bundles in `harvests/` (283 image entries); (2) the `item.get` / `profile.getAi` captures (push/323, push/249); (3) the `@img` or URL a verified spent manifest wrote; (4) `state/skyglass_fx/asset_ids.json` for push/320 |
| **EXISTS IN REPO, NOT UPLOADED** | a finished, preflighted export is committed but the live record still shows a placeholder | path under `art/`; no idmap entry; the creating manifest wrote a placeholder |
| **NEEDS ART** | nothing usable exists | — |
| **REDRAW / RECOLOUR** | a base image exists and the new asset is derived from it | base path or live URL |
| **NOT NEEDED** | cut, retired, superseded or covered by a shared asset | the ruling, listed in §N |
| **UNCERTAIN** | the docs do not settle whether an asset is needed | flagged; never guessed into a count |

**The live placeholder** is `https://uploadthing.b-cdn.net/f/630cf6e7-c152-4dea-a3ff-821de76d7f5a_default.webp` (the
engine default). A real upload is a `ui0arpl8sm.ufs.sh/f/…` or `utfs.io/f/…` URL.

**Capture gap.** The push/323 item capture read the 766-item seed index; the live catalogue had 873. The Skyglass event
items created in push/260, 270, 271 and 274 are newer than the seed, so their live images are taken from the verified
spent manifests that created them, not from a capture. Nothing below claims a live image without one of the four
evidence types.

## Specs per asset type (from `25x_DATA_art_spec.json`; the spec governs, this is a summary)

| Type | Client field | Aspect | Min width | Recommended source | Key / alpha | Format, ceiling |
|---|---|---|---|---|---|---|
| SCENE_BACKGROUND | quest / objective `sceneBackground` | 3:2, stretched | 512 | 1536 x 1024 | none; no people or creatures | webp, 460,800 B |
| SCENE_CHARACTER | `sceneCharacters[]` | 2:3 full body or 1:1 bust, width-scaled | 341 | 682 x 1024 / 682 x 682 | lime (magenta for green subjects) | webp, 460,800 B |
| AI_AVATAR | `userData.avatar` | 1:1, stretched | 320 | 640 x 640 | lime (the Skyglass batch used magenta) | webp, 460,800 B |
| ICON | `item.image`, item-variant image, `quest.image` | 1:1, stretched; rarity frame composited behind | 160 | 256 x 256 | lime; alpha required; small margin so the frame reads | webp, 460,800 B |
| JUTSU_ICON | `jutsu.image` | 1:1 | 160 | 256 x 256 | designed opaque background allowed (RUL-2026-10-14-001) | lossless webp |
| STATIC | `effect.staticAssetPath` (gameAsset) | 1:1, circular mask | 128 | 256 x 256 | lime | webp |
| ANIMATION | `appear/static/disappearAnimation` (gameAsset) | vertical strip, square frames | 112 per frame | — | lime | webp, 460,800 B per strip |
| Badge | `badge.image` (URL ≤ 191 chars) | not in the art spec; the Crownbreaker badge was made as ICON 256 | — | — | — | — |

Notes:
- The Skyglass FX strips are drawn natively at **50 px frames** (`art/skyglass_boss_fx/animate.py`: the CDN serves them
  at `?width=50`), below the spec's 112 px content-list minimum. The 10 live assets went out that way; the remaining
  strips follow the same builder. Flagged for awareness only.
- Every new animation is created hidden, unhidden by id (law 16c), and gets a new filename per revision (law 32).
- Style for every image: Edo-era Japanese fantasy ninja pixel art anchored on the original crew (RUL-2026-10-26-002;
  `docs/design/ghost_ship_art_bible/`), the shared Skyglass emblem (four-point star in a diamond or circle,
  RUL-2026-10-26-004), skyglass pale cyan as the accent.

---

## A. Scene backgrounds

Every Skyglass quest reuses the ten approved ship scenes. RUL-2026-10-28-007: "No existing art is redrawn; the story
bends to it … The ship scenes are the Core holding the wreck's interior as it was."

### A1. Existing, live (reused; no art needed)

| Scene | Used by | Status | Evidence (upload key) |
|---|---|---|---|
| exterior_keel_walk | Foundry and Archive arrivals | EXISTS LIVE | `scene_bg_ghost_ship_exterior_keel_walk.webp` → `QfsAnXSp9QG0AuwbQywCW` (push/265, 266) |
| lower_hull | Archive, Foundry, Low Tide (breach), The Fall (gun deck), Burning Heading | EXISTS LIVE | `…YURJ0pHtoKgrYldRWJcD6vE10SjNsXHeA9pVMfQi` |
| hold | Foundry, Low Tide (flooded hold), The Fall and Burning Heading (the break); Crownhold division 2 placeholder | EXISTS LIVE | `…YURJTdaBvI5IU29dZYJPoOKSh5vmlqatMub3EigH` |
| reconstruction_chamber | Archive; Crownhold division 3 placeholder | EXISTS LIVE | `…YURJRiFRQZ0udmODoNtpa0FMcwI4k2Eq7nJhyvjl` |
| quarantined_archive | Archive, Sealed and Rotted Reliquary | EXISTS LIVE | `…YURJpo8lFZubKBAOsGCHyl3Sk0mZFrgWPUdjMJ75` |
| cache_site | Buried Cache, Watch landing, Low Tide beach | EXISTS LIVE | `…YURJyX6gwPukVH2MI5Lo4ehEfAXvZdcmtWqPg7rp` |
| chart_room | Captain's Watch | EXISTS LIVE | `…YURJqpbYjW5dkOZgJQ8mGRcdx3SsWvPelyYFTt5V` |
| deck_b | Watch, Night Watch, The Fall, Burning Heading | EXISTS LIVE | `…YURJcoxkatSnxBpQqGNDcTHbLmYz8uXAl3oa54ti` |
| helm | Watch; Crownhold division 5 placeholder | EXISTS LIVE | `…YURJIp0fIvxfOewksxBoS1HQCihpL7c42Ky9uUFv` |
| command_observation_gallery | Watch; Crownhold division 4 placeholder | EXISTS LIVE | `…YURJ8ZwqPukkp45TvAnoIBa0rtCf1lbyXYjVKQ2q` |

Scene assignments for the new runs are from `SKYGLASS_TEXT.md` §2 (`(scene: …)` tags) and `state/skyglass_hunts/hunts.py`.

### A2. Crownhold scenes (new locations; placeholders live)

Crownhold currently borrows four ship scenes (`push/crownhold.gen.py` `SCENE`: "placeholders … until Crownhold's six
scenes are drawn"). The art batch specifies 19 (#27-#45). All are **NEEDS ART**, SCENE_BACKGROUND, prompts written in
the batch handoff (each lists the nodes that use it).

| # | Scene | Delivery file |
|---|---|---|
| 27 | Crownhold gate | `scene_bg_crownhold_gate.webp` |
| 28 | Armory proving hall | `scene_bg_crownhold_proving_hall.webp` |
| 29 | Ordnance store | `scene_bg_crownhold_ordnance_store.webp` |
| 30 | Test gallery | `scene_bg_crownhold_test_gallery.webp` |
| 31 | Armory command shrine (file says "terminal"; RUL-2026-10-26-004 renames it) | `scene_bg_crownhold_armory_terminal.webp` |
| 32 | Forge wall | `scene_bg_crownhold_forge_wall.webp` |
| 33 | Archive of impressions | `scene_bg_crownhold_archive_of_impressions.webp` |
| 34 | Vat halls (sealing jars, RUL-2026-10-26-005) | `scene_bg_crownhold_vat_halls.webp` |
| 35 | Research command shrine | `scene_bg_crownhold_research_terminal.webp` |
| 36 | Reconstruction theatre (the recall chamber) | `scene_bg_crownhold_reconstruction_theatre.webp` |
| 37 | High Command signal room | `scene_bg_crownhold_signal_room.webp` |
| 38 | Planning hall | `scene_bg_crownhold_planning_hall.webp` |
| 39 | Honor guard corridor | `scene_bg_crownhold_honor_guard_corridor.webp` |
| 40 | High Command shrine | `scene_bg_crownhold_high_command_terminal.webp` |
| 41 | The Second's office (file says Grand Marshal) | `scene_bg_crownhold_marshals_office.webp` |
| 42 | Sanctum gate | `scene_bg_crownhold_sanctum_gate.webp` |
| 43 | Sanctum antechamber | `scene_bg_crownhold_antechamber.webp` |
| 44 | Outer ring and shrine | `scene_bg_crownhold_outer_ring.webp` |
| 45 | Throne room (the Crowned Captain's fight; the order carved behind the throne, the mission line blank stone: story bible) | `scene_bg_crownhold_throne_room.webp` |

**Uncertain:** the Crownhold package shot list says six scenes; the batch says 19. The batch prompts predate
RUL-2026-10-26-004/-005 in places (terminal / tank wording), so re-check each prompt against the Edo pass before its
session. The placeholders work, so these are not release-blocking unless the director says so.

### A3. Scenes for the new quests (reuse assumed; flagged)

| Quest | Need | Status |
|---|---|---|
| Wreck Sighted (intro, public) | a background for its 3 dialog nodes | **UNCERTAIN**: no scene is named in `SKYGLASS_TEXT.md` §1. `cache_site` (a beach) or `exterior_keel_walk` (the wreck on the sand) fit the text; no new art assumed |
| The Haul, 6 quests | backgrounds for step dialogs | **UNCERTAIN**: `haul_spec.json` and the text name none. `hold` / `lower_hull` fit "below the gun deck" and "the lower stores"; no new art assumed |
| Steeping, 2 special quests | the rot pool | **UNCERTAIN**: no scene named; `hold` (the flooded hold where the Core Horror lives) fits |
| Walked Every Deck, Proving Ground | achievement / hidden test | none needed |

### A4. Not needed

The 14 Skyglass scene redraws in the batch (#66-#79: wreck keel and hatch, flooded intake, cooling racks, pour hall,
crucible chamber, rebuilding lower hull, reconstruction chamber, quarantined archive, night cove landing, chart room,
open deck, helm, observation gallery, three coves and the stone shrine). Each prompt takes an existing ship scene as its
composition base, so it is a regeneration of existing art, which RUL-2026-10-28-007 rules out. **Uncertain:** four of
them (the Foundry's intake, racks, pour hall and crucible) and the three-coves shore depict rooms no current scene shows;
the director may want to revive those as new locations.

---

## B. Scene characters (dialog portraits)

| Asset | Used by | Status | Evidence / spec |
|---|---|---|---|
| Sealwright portrait | Archive | EXISTS LIVE | gameAsset `b_K8qdNI651fTsRn9tfkk` (`hunts.py` PORTRAIT) |
| Oathkeeper portrait | Captain's Watch | EXISTS LIVE | gameAsset `6iwMYC8WTCGJTf2QIYfBz` |
| The Captain portrait | Captain's Watch | EXISTS LIVE | gameAsset `xm3F2YXkNPeLWHRAUnbmF` |
| Crowned Captain portrait | available for Crownhold (its nodes currently use none) | EXISTS LIVE (image) | `scene_char_ghost_ship_crowned_captain_portrait_b.webp` → `…YURJmD4DcyHE4IMO5Goa7cgLxPJ0VC6lU8vbt1Ap`; its gameAsset id is not recorded in the repo |
| **The salvager** (Wreck Sighted) | the intro quest; public quests require scene characters (quest.md) | **NEEDS ART** (RUL-2026-10-29-057 item 7) | SCENE_CHARACTER, CIVILIAN register, 2:3 full body, lime key. **Prompt hint** (`SKYGLASS_TEXT.md` §1): a coast salvager, a woman, soaked and salt-stained, pushing a wet chart into the player's hands; Edo-era working clothes (tenugui, rolled sleeves, straw sandals), no insignia |

Not needed: portraits for the new chart runs. Battle Pyramid runs are not public, and the live hunts set
`sceneCharacters: []` on every node except the three portraits above. **Uncertain** only if the director wants the
Wayfinder, First Blade or Arsenal Keeper to speak on screen in the new runs (no portrait of them exists).

---

## C. AI battle avatars

### C1. Ghost Ship crew (live; reused by the Wreck, its level-50 copies, the hunts, the chart runs and The Haul)

All EXISTS LIVE (live `profile.getAi`, push/249 capture, `ai-sprite-…` URLs; uploads in the idmap):

| AI | Live id | Also covers |
|---|---|---|
| Deck Warden | `texZaFi42S3EvJZBwQ8cd` | every Crownhold regular's placeholder |
| Arsenal Keeper | `2OXJEXoktxJcjqMkE851g` | The Fall's fire source (his echo at the powder magazine, RUL-2026-10-28-027); Foundry Warden and Armsmaster placeholders |
| Wayfinder | `v7T9_XdGMfP46em0dPuBc` | |
| Oathkeeper | `0PZU_FvlbM3ErYGlD5r56` | |
| First Blade | `d6g0mOM7RBSsYI1hrUVT9` | |
| Sealwright | `RBW5KsIXmTGR710D2y2Y7` | Replicant Zero placeholder |
| Skyglass Sentinel | `3V_gdHYaclMB1gTyOPAbV` | |
| Core Horror | `AQi-bHJ-5tHXtxrnc0P9E` | the steeping copy; the Reliquary and Fall copies |
| The Captain | `QY69h271Nx9uHrBeR6jwW` | The Second placeholder; the Burning Heading ally |
| Crowned Captain | `fDU9jCPZtH7YHbdQPO9RF` | the Crownhold boss `7QofodAiUwIoM-voiA2p6` uses this sprite **unchanged** (RUL-2026-10-28-003/-007) |
| Seal Charge | `wTgO-Q32caSSd0is1QIS7` | Haul stationary fuses (RUL-2026-10-29-044 item 6) |
| Core Canister | `frc9LTxqQlM7mncG4VZGK` | Haul stationary fuses |

New AI records that **reuse** these (no art): the Wreck's dungeon and level-50 copies, the Reliquary's static hazard
echoes, the Haul's guard copies, the Core Horror steeping copy. **Uncertain:** the Haul's named guards (the Trophy
Warden, the Stores Ward) have no avatar decision in `SKYGLASS_THE_HAUL.md`; reuse is assumed.

### C2. Foundry Warden

| Asset | Status | Evidence | Note |
|---|---|---|---|
| Foundry Warden (`81lnIP-q97gItQYWl5vWD`, Drowned Foundry boss) | **REDRAW** (base in repo, not uploaded) | `art/skyglass_event_icons/avatars/avatar_skyglass_foundry_warden.webp` (1004 px); live record created with the Arsenal Keeper's sprite (push/262) | RUL-2026-10-26-002 item 3 put it in the redo queue (brown, off-palette). RUL-2026-10-29-029: his tool is a **forge maul**. **Uncertain:** whether RUL-2026-10-28-007's "no redraws" freezes the repo version (it was never live) |

### C3. Crownhold (20 AIs, `state/crownhold/ids.json`; all live with borrowed crew sprites)

Names per RUL-2026-10-26-003; style per RUL-2026-10-26-001 (chakra-impression ninjas in the crew's outfit language,
no seams, no threads, no crowns). AI_AVATAR, magenta key in this batch.

| # | Officer (live username) | Role | Status | Path |
|---|---|---|---|---|
| 8 | Crown Armsmaster | division 2 commander | EXISTS IN REPO, NOT UPLOADED | `art/crownhold/avatar_crownhold_master_of_arms.webp` (redone 2026-10-26, approved) |
| 9 | Replicant Zero | division 3 commander | EXISTS IN REPO, NOT UPLOADED | `art/crownhold/avatar_crownhold_replicant_zero.webp` |
| 10 | The Second | division 4 commander | EXISTS IN REPO, NOT UPLOADED | `art/crownhold/avatar_crownhold_the_grand_marshal.webp` |
| 11 | Crown Trialmaster | regular | EXISTS IN REPO, NOT UPLOADED | `avatar_crownhold_proving_proctor.webp` |
| 12 | Crown Tagwright | regular | **NEEDS ART** | `avatar_crownhold_ordnance_quartermaster.webp` (prompt in batch) |
| 13 | Crown Lancer | regular | **NEEDS ART** | `avatar_crownhold_prototype_lancer_unit.webp` |
| 14 | Crown Duelist | regular | EXISTS IN REPO, NOT UPLOADED | `avatar_crownhold_calibration_duelist.webp` |
| 15 | Crown Archivist | regular; also the Archive's alarm guard (RUL-2026-10-28-013) | EXISTS IN REPO, NOT UPLOADED | `avatar_crownhold_skyglass_archive_keeper.webp` |
| 16 | Crown Binder | regular | EXISTS IN REPO, NOT UPLOADED | `avatar_crownhold_impression_containment_warden.webp` |
| 17 | Crown Echo | regular | EXISTS IN REPO, NOT UPLOADED | `avatar_crownhold_unstable_echo_subject.webp` |
| 18 | Crown Stonebound | regular; also the Sealwright's summon (RUL-2026-10-28-013) | EXISTS IN REPO, NOT UPLOADED | `avatar_crownhold_failed_reconstruction_prototype.webp` |
| 19 | Crown Signaller | regular | EXISTS IN REPO, NOT UPLOADED | `avatar_crownhold_command_signal_adjutant.webp` |
| 20 | Crown Tactician | regular | EXISTS IN REPO, NOT UPLOADED | `avatar_crownhold_high_command_staff_tactician.webp` |
| 21 | Honor Guard | regular | **NEEDS ART** | `avatar_crownhold_honor_guard_commandant.webp` |
| 22 | Crown Runner | regular | **NEEDS ART** | `avatar_crownhold_strategists_aide_de_camp.webp` |
| 23 | Crown Vanguard | regular | **NEEDS ART** | `avatar_crownhold_sanctum_vanguard.webp` |
| 24 | Crown Herald | regular | **NEEDS ART** | `avatar_crownhold_directive_herald.webp` |
| 25 | Last Watch | regular | **NEEDS ART** | `avatar_crownhold_last_watch_executor.webp` |
| 26 | Crown Sealbearer | regular (carries the Skyglass-emblem tablet, RUL-2026-10-26-004) | **NEEDS ART** | `avatar_crownhold_order_bearer_of_the_sanctum.webp` |
| — | The Crowned Captain | division 5 boss | EXISTS LIVE (crew sprite, unchanged) | C1 |

Uploading the 11 finished avatars needs an avatar-edit manifest; `push/skyglass_art_swaps.gen.py` has no rows for them
yet (git log mentions SWAPS rows at `49ad6937`; the current file carries only the four icons in D2).

---

## D. Item icons

ICON target throughout. Rarity per RUL-2026-10-29-058; seal colours per RUL-2026-10-28-028 item 4 (see L1).

### D1. Existing, live

| Item | Live id | Image | Evidence |
|---|---|---|---|
| Skyglass Coffer | `THo7rfzP-S82_43aN8fs3` | `icon-skyglass-coffer.webp` | push/260; idmap `psAydgBQxvbwe5QT82JzK` |
| Elemental Tool Pouch (the Katon Tool Pouch record) | `D0gtI5dOgj2dFO4VexsLJ` | `icon-tool-pouch-katon.webp` | push/260; idmap `kRUoJzyTLGbTdG-dRP_zU`. See D4 |
| Chart of the Drowned Foundry | `pY-0O5Gs2n89pf0kYb5J2` | `icon-chart-drowned-foundry.webp` | idmap `qKeetzpaN_8TBOv_XISiq` |
| Chart of the Quarantined Archive | `cRZT41zm5vhPTQwwn8vtv` | `icon-chart-quarantined-archive.webp` | idmap `pDUTNFUKXRIPMj5umfUsn` |
| Chart of the Captain's Watch | `aHFNuo5RkKpDcaOBLIKiu` | `icon-chart-captains-watch.webp` | idmap `mjyb69AblnvT0txBu86k4` |
| Lastlight Lantern | `jCJv4N3JSiihuqnK0jJ7t` | `icon-skyglass-signal-beacon.webp` | idmap `e4eNC9JdUPrchiJKcMGUX` |
| Medicine Inro | `ixEKlJ0MmDrX7JoMNJVhi` | `icon-medicine-inro.webp` | capture `…YURJP0FMbypKeUGyX2kj6u45AOQiSa1zYH0mqZoc` |
| Sage's Strongbox | `h-d58UCSuHN8EZKbLjT5R` | `icon-sages-strongbox.webp` | capture `…YURJZSxRRoaYQrBIUTu69nkMxWmS4ah0O7LVCp8b` |
| Skyglass Filament, Skyglass Serum (`XhilCv1Hq4eNt-Wddok-m`), Fragment of the Skyglass Crown (`ayiRmSjWs05lMPyL3G-1d`), Skyglass Katana, Skyglass Crystal, The Skyglass Crown (`yTS9TSpr_QLnh_3zmEpGg`) | — | `icon_ghost_ship_skyglass_*.webp` | idmap; captures for Serum, Fragment, Crown |
| 8 profession chests (Common / Rare / Epic / Legendary Hunter's and Gatherer's) | e.g. `KwgjMOya2XT6uYsgXbsh6`, `nAAfu3ya-dkVaZeH7LycZ` | live images, one per tier, shared by the Hunter's and Gatherer's chest of that tier | capture push/323 |

The profession chests are existing live items (The Haul pays them as plain `reward_items`); no new chest art. The Lion
Token (`FG4xYkI8UmRrJCdD3yPxI`, live image) is a reference only: the Skyglass Token must not read like it.

### D2. Finished, in repo, not uploaded (`push/skyglass_art_swaps.gen.py` → push/275, built but never run)

| # | Item | Live id | Live shows now | Repo export |
|---|---|---|---|---|
| 1 | Sealed Treasury | `Ma8S90Nmbi0Xvm4u4FzJh` | a borrowed image (`…YURJWLNYJ7Svszvj71yaSYC0MDOmbko5q9JAGuLH`) | `art/skyglass_event_icons/exports/icon-sealed-treasury.webp` |
| 2 | Archive Chart Case | `B48dTRsoLJGKBWIUbeUoG` | a borrowed image (`utfs.io/f/…YURJC0gnIF26…`) | `…/icon-archive-chart-case.webp` |
| 3 | Chart of the Buried Cache | `nbLC37UzBamthKXvZsgQB` | the Foundry chart icon | `…/icon-chart-buried-cache.webp` |
| 4 | Unmarked Cargo | `KzITKJ5BUQRz5QuYWw-0B` | the Coffer icon | `…/icon-unmarked-cargo.webp` |

RUL-2026-10-26-002 item 3 keeps these four. **Uncertain:** the Buried Cache chart was drawn when it was COMMON (push/270);
it is now a Rare chart (RUL-2026-10-29-058) with a cyan seal (L1). Check the export's seal before the swap runs. The Buried
Cache **quest** image also shows the Foundry chart icon and is not in the push/275 rows (J).

### D3. New icons, NEEDS ART

| Item | Rarity / seal | Where used | Prompt hint (design / text source) |
|---|---|---|---|
| Tide Chart | Common, plain | easy and endgame Wreck drop; Night Watch pick; Wreck Sighted reward; Low Tide Run entry | "The Wayfinder's tide table, marked where the low tide opens the wreck's lower hull" (TEXT §4.1); chart family of the Foundry chart (rolled dark chart paper, pale lines) |
| Watch Roster | Common, plain | Wreck drop; Low Tide pick; Night Watch entry | "your name on the duty roster" (loot tables §5): a duty board or roster scroll with names, one fresh |
| Reliquary Seal | Epic, gold | Archive ending, Archive Chart Case, Crownhold ending; Sealed Reliquary entry; steeping | "The seal of the iron reliquary chained behind the Sealwright" (TEXT §4.1): an iron seal plate on a chain, skyglass at its heart |
| The Last Heading | Epic, gold | Watch ending, Chart Case, Crownhold ending; The Fall entry; steeping | "The Wayfinder's final course: the night the ship came down" (TEXT §4.1): a scorched chart with one heading line |
| Core Rot | Rare, cyan | Wreck, common runs, Core Horror runs, breaking the seal, failed rare runs; steeping reagent | "dark, wet timber and rope, and skyglass gone cloudy" (TEXT §4.2). Generator caution: amorphous chunks fail (skill); frame it as a holdable lump bound in rope, or a stoppered jar |
| The Little Horror's Jar | Legendary | endgame Wreck, 5%, once per player (RUL-2026-10-29-054) | "the ship's mascot, sealed in a jar … This is what came back" (TEXT §4.2): a sealed jar with a small rot-and-skyglass creature, one tooth too many, pressed to the glass |
| Galley Stores | Rare, cyan | easy Wreck 10%; four picks; The Fall ×3; chest of chests | "The galley still stocks a larder for a crew that does not eat" (story bible): a ship's provisions crate or rice sack with the Skyglass star stamp |
| Skyglass Token | Legendary | Archive, Watch, rare-run picks; chest of chests; Crown's Hoard | "A token pressed from clouded skyglass and stamped with the four-point star" (TEXT §4.3) |
| Crown's Hoard | Legendary | Crownhold pick | "Crownhold's own coffers, treasury and jars, gathered beneath the throne" (story bible). **Not on any "new art" list** in the loot tables (flag); a placeholder would otherwise ship |
| 7 boss variant tokens: Captain's Command Fan, Rot-Bloom Reaper, Warden's Forge-Fists, Wayfinder's Heading, The First Blade, Sealwright's Seal, Crownbreaker | Legendary | endgame Wreck 5%, once per player (Captain, Core Horror; RUL-2026-10-30-060); boss runs 1/2/4%; Walked Every Deck (Crownbreaker) | loot tables §5d: "7 trophy token icons". Names carry the variant alone, no "Variant" suffix (RUL-2026-10-29-057 item 1). No art line is written; the token story lines are in TEXT §4.3. **Uncertain:** seven distinct icons, or one token base with seven variant motifs (cheaper; only the motif changes) |
| Haul pages, base icons ×2: Ledger Page, Stores Manifest | Legendary | endgame Wreck 2.4%, Rare-chart endings 1.5% each (RUL-2026-10-30-060, replacing RUL-2026-10-29-053); Haul entry | TEXT §3.2 stories: a torn ledger page from the Arsenal Keeper's ledger (due dates crossed out); a quartermaster's manifest with skyglass grown through the lines. See D4 for the other four pages |
| Countermand | AI-held item (the Crowned Captain), placeholder | `W3lOjQhhIPUYPkIZmiNum` (push/271 placeholder) | batch #48: the command seal of Crownhold, now the Skyglass emblem (RUL-2026-10-26-004). Low priority: players see it only in battle |

### D4. Recolours / redraws

| Item | Base | Kind | Note |
|---|---|---|---|
| Rotted Reliquary Seal | Reliquary Seal (D3) | RECOLOUR | Legendary, rot-green seal; "soaked in the Core's rot" (TEXT §4.1). Loot tables §5 "2 tainted chart recolours" |
| The Rotted Heading | The Last Heading (D3) | RECOLOUR | name ruled by RUL-2026-10-29-057 item 2 |
| Ledger Page: The Bone Store, Ledger Page: The Snare Room | Ledger Page base | RECOLOUR | **Uncertain** (no Haul art is specified anywhere): one icon per page or one per profession. Three distinct pages help tell drops apart in the inventory |
| Stores Manifest: The Ore Vault, Stores Manifest: The Bloom Cellar | Stores Manifest base | RECOLOUR | as above |
| Elemental Tool Pouch | live Katon pouch icon | REDRAW (neutral) | `push/elemental_pouch.gen.py`: "the Katon icon stays until a neutral pouch is drawn". **Uncertain:** RUL-2026-10-28-007 vs a fire-themed icon on an all-element pouch; director's call |

---

## E. Variant skin images (19)

Each is the image on an `ItemVariant` row of a live crafted weapon (ICON target; Forge variant builder: image `@img` or
URL ≤ 512). Art rule (RUL-2026-10-29-049, loot tables §5d): keep the base weapon's silhouette; skyglass only as inlay
and accents; the Skyglass Katana stays the only all-crystal blade; no variant reads as a crystal sword. Use the base's
live icon as the SUBJECT reference. Art lines are in `SKYGLASS_TEXT.md` §5 (subject only; the item-icon scaffold adds
style, framing and key). All **NEEDS ART**.

### E1. The 12 Skyglass variants (Skyglass Token)

| Base (live id, rarity) | Variant | Prompt hint (TEXT §5.1, abridged) |
|---|---|---|
| Aetherion (`PhP5ZEF5iVa97jcumJ15c`, L) | Gale-Watch Aetherion | thin cyan skyglass vein down the fuller; sailcloth grip; small four-point star pommel |
| Thornsilver (`MQ5mJqH-5MkQdtLGSZ5nb`, L) | Tidewater Thornsilver | wet-dark steel; a row of small skyglass beads on the spine; salt crust at the guard |
| Night's Testament (`osJq3k77YPGoFWgof12FQ`, L) | Night Watch Testament | blackened blade unchanged; one small cyan star in the crossguard; no crystal on the blade |
| Stormrender (`cLXXf8RJv5l9B_gGsYN2a`, L) | Mast-Lightning Stormrender | short skyglass rod upright in the crossguard; cyan crackle on the ricasso only |
| Oathbinder (`ttwbJ6ZA5Id-OuBludM27`, L) | Roll-Call Oathbinder | the chain's white prayer knots become small cyan beads |
| Ink of the Void (`wE1QeldWTjls2Cf43cFjf`, L) | Chartline Ink of the Void | fine cyan chart lines and a compass mark along both limbs |
| The Unwritten (`m0RZDUDnwQu_0BtOJgHi9`, L) | The Unwritten Order | paper ribs written with faint orders, one blank line; edge sealed with cyan wax |
| Gaea's Embrace (`-LzgdTM1yTjlezOyjd-6H`, E) | Keelstone Embrace | orange tip crystal recoloured pale cyan; two iron bands on the shaft |
| Warden's Bracers (`qTzWEb6tFBv8dl15ztqDO`, E) | Drill-Count Bracers | tally notches across the knuckles, a tiny cyan stud in each |
| Eclipsed Dawnblade (`MbPhG5El3UYjS5Bk2K3Bl`, E) | Lastlight Dawnblade | small lantern-shaped skyglass core at the blade's base, light contained |
| Zephyr's Whisper (`CBp4scJi9XzMKRqxpshwT`, E) | Skysail Whisper | green crystal recoloured cyan; rigging cords between the ribs |
| Yuki's Frostbite (`Z-JdppXvrSokRymXavpOw`, R) | Hullbreaker Frostbite | dark ship's-timber haft with iron rings; skyglass in the cheek of the head, not the edge |

### E2. The 7 boss variants (one token each)

| Base (live id) | Variant | Prompt hint (TEXT §5.2, abridged) |
|---|---|---|
| The Unwritten (`m0RZDUDnwQu_0BtOJgHi9`) | Captain's Command Fan | a gunbai war fan in the fan's footprint: black-lacquered paddle, iron rim, short haft, four-point skyglass star at the centre, faint cyan cracks |
| Oathbinder (`ttwbJ6ZA5Id-OuBludM27`) | Rot-Bloom Reaper | wet dark rope chain; cloudy milky skyglass growing like barnacles on the blade's back; rot-stained haft |
| Warden's Bracers (`qTzWEb6tFBv8dl15ztqDO`) | Warden's Forge-Fists | soot-black forged iron, blunt maul-head knuckle plates, thin seams of cooled skyglass |
| Stormrender (`cLXXf8RJv5l9B_gGsYN2a`) | Wayfinder's Heading | small skyglass compass rose at the crossguard; etched route line down the fuller |
| Aetherion (`PhP5ZEF5iVa97jcumJ15c`) | The First Blade | long grey-blue cord bound round the grip, ends trailing as in wind; short skyglass inlay at the blade's base; brass fittings |
| Whispering Dawnblade (`mqCCZGSfXUNL02B4H6C9R`, E) | Sealwright's Seal | dark seal script engraved along the whole blade; round skyglass seal disc at the pommel |
| Thornsilver (`MQ5mJqH-5MkQdtLGSZ5nb`) | Crownbreaker | three short broken frost-point shards of pale skyglass in the crossguard; plain steel blade |

Note: six bases carry two variants each (Aetherion, Thornsilver, Stormrender, Oathbinder, The Unwritten, Warden's
Bracers); the two on one base must read clearly apart at 125 px. The Sealwright's base is **Whispering** Dawnblade
(`mqCCZGSfXUNL02B4H6C9R`), not the catalogue's **Eclipsed** Dawnblade; both are live items. Settled by RUL-2026-10-30-060
item 8.

---

## F. Jutsu icons

| Jutsu | Who sees it | Status | Evidence / note |
|---|---|---|---|
| **Lastlight** (`0F-68bxOXW_LkJnXV0lwT`) | players: the Crownhold pick jutsu | **NEEDS ART** (#6, `icon-jutsu-lastlight.webp`) | live placeholder = the Lantern item icon (push/261) |
| **Little Maw** (the Little Horror's signature, `requiredPetSpeciesId`) | players: the pet's loadout | **NEEDS ART** | not on any art list (flag). Hint: the Core Horror's maw in miniature, small and oddly cute |
| The Last Directive (`GHFMU_DDKvBBp5BEuTeah`) | AI only (the Crowned Captain) | NEEDS ART, low priority (#46) | live placeholder = engine default (push/271) |
| Extermination Order (`EqZsaqser8c2-KpVCaXk_`) | AI only | NEEDS ART, low priority (#47) | same |
| Steady the Helm; the shared library (10 marks, about 6 blasts, the Lowered Guard); the 6 bespoke signatures; the 6 crew additions; Recall and Called to the Archive; The Crown's Will; Spreading Fire I-III; Crown Stonebound's Erupting Ground copy | AI only | **UNCERTAIN, assumed placeholder** | the harness specs (`charts_spec.json`, `hunts_spec.json`) carry the engine default image; no design doc asks for icons. If wanted, about 37 icons, best as a family of 4-6 shared mark/blast glyphs |

---

## G. Badge

| Asset | Status | Evidence |
|---|---|---|
| **Crownbreaker** badge (Crownhold pick; the badge greys out once held) | EXISTS IN REPO, NOT UPLOADED | `art/crownhold/icon-badge-crownbreaker-v2.webp` (256 px lossless, 105,698 B; the frost crown in a Skyglass round border, director 2026-10-28). The director uploads it when creating the badge by hand; the badge id is still pending (push/319 "Before it runs") |
| Crownbreaker v1 (Arakane's gold crown) | NOT NEEDED | retired with Arakane (RUL-2026-10-28-007; README of `art/crownhold/`) |

"Crownhold badge" in the request is this badge: Crownhold has no second badge.

---

## H. Battle animations and FX

Shapes and palettes: `SKYGLASS_BOSS_ANIMATIONS.md` (heavy = ember red, control/lock = violet, lingering = bile green,
safe = skyglass cyan). Every burst window uses the same tile (RUL-2026-10-28-028 item 6). Shared blasts carry the shared
animation (Boss Fights §5a).

### H1. Danger language, live (push/320 + 321, unhidden)

| Asset (gameAsset id) | Type | File |
|---|---|---|
| Skyglass Mark - Heavy (tile) `dGCN9ZaoyXwDK9E3ZuWgU` | STATIC, under the characters | `tile_heavy_v3.webp` |
| Skyglass Mark - Binding (tile) `M2oqurvH5jYkuCeDafnFK` | STATIC | `tile_control_v3.webp` |
| Skyglass Mark - Lingering Pool (tile) `PoG_KDERWlvyj7MsKSDW2` | STATIC | `tile_linger_v3.webp` |
| Skyglass Mark - Safe (tile) `-hIV18piGe0EcC0u6eN8d` | STATIC | `tile_safe_v3.webp` |
| Heavy glint `dL1vh_PNbZQ9m6nYwGnFa` · Binding glint `ZZ2YrtIAxfnlHAzOHXSgl` · Pool bubbles `qlGYJizxxxdd794Jea6lB` · Safe floating emblem `v9nA0cPU5NXxBXoONhdLH` | ANIMATION loops | `anim_*_glint_v3.webp` |
| Skyglass Blast - Eruption `Z9j8J7ZmAjiaxH2S4nDy8` | ANIMATION one-shot (the shared heavy blast: Ring, Rows, Scatter, Lines, Splash, Short Line) | `anim_dt_heavy_v2.webp` |
| Skyglass Blast - Crystal Shard `TAu9k8ifgteP6HBofoKn7` | ANIMATION one-shot | `anim_dt_shard_v2.webp` |

These cover the marks and minor marks (RUL-2026-10-28-024: "visuals reuse the existing mark and blast tiles"), the
lingering pools (Core Rebuilds, Pour Line's burning glass), and the shared blasts. So the design ids ch_collapse,
ch_rupture, fw_pour, st_tide and Shardstorm resolve to Eruption / Crystal Shard through the library: **NOT NEEDED** as
separate strips.

### H2. Boss set pieces, in repo, NOT UPLOADED (15 strips, `art/skyglass_boss_fx/exports/`, `boss_fx.py`)

| Strip | Design id / move | Notes |
|---|---|---|
| `anim_maw_v1.webp`, `anim_maw_field_v1.webp` | ch_maw, Maw of the Deep | per-hex and arena-field versions; also the Little Horror's **Little Maw** (Pets doc) |
| `anim_quench_v1.webp` | fw_quench, Quench | |
| `anim_command_absolute_v1.webp`, `anim_command_absolute_field_v1.webp` | cc_command_absolute | |
| `anim_crownfall_v1.webp` | cc_crownfall | |
| `anim_broadside_v1.webp`, `anim_broadside_field_v1.webp` | cp_broadside | |
| `anim_ships_bell_v1.webp` | cp_bell_toll, Ship's Bell | |
| `anim_crimson_strike_v1.webp` | cp_final_command, Final Command (Captain and Crowned Captain) | |
| `anim_chain_wrap_v1.webp` | Keelbind, Chain Hook, Mould Cage | |
| `anim_recall_v1.webp` | cc_recall; Called to the Archive reuses it | |
| `anim_crown_aura_v1.webp` | cc_crown_aura, The Crown's Will (loop; keeps the portrait clear) | `boss_fx.py` labels it "Crown's Will / Last Directive" |
| `anim_rot_claw_v1.webp` | ch_claw, Splintered Grasp | |
| `anim_exposed_v1.webp` | the one shared window: ch_exposed, fw_cracked, st_exposed, sw_lowered, the First Blade's and the Second's windows | RUL-2026-10-28-028 item 6 |

Each needs an asset-create manifest, then the unhide (as push/320 → 321), and the Proving Ground test-play
(RUL-2026-10-28-028 item 7). Preview: `docs/design/skyglass_boss_fx/boss_reel.mp4`.

### H3. NEEDS ART (named in the design, no strip exists)

| Design id | Move / purpose | Kind | Hint (Boss Fights / Boss Animations) |
|---|---|---|---|
| shared violet blast (dt_control) | Binding: Seal Cross (Script Lines, Replicant Zero's Jar Seals); the Archive Lock payoff | detonation | "chains snap up and lock, ink splash". **Uncertain:** `chain_wrap` or `command_absolute` may be reused instead |
| cp_command | Hold the Line / Unbroken Command; the Ward of Command banner on the Captain | aura (loop) | "a command banner snapping in a wind behind him" |
| cp_gunwale | Raise the Gunwale barrier (the phase-2 transition) | barrier sprite | "timber-and-seal wall". **Uncertain:** whether the barrier tag's sprite is a STATIC gameAsset or an ANIMATION |
| cc_phase_shift | the Crowned Captain at 60% / 30%; recoloured for the Captain's Last Stand; Ruin Refrain's pulse | cast flourish | "crown flare and shockwave" |
| cc_hexweave | Hexweave debuff | hit | "violet sigil" |
| ch_enrage | The Core Rebuilds (under 50%) | aura | "rot glow and drip on him" |
| ch_bile_spit | Bilge Spit (plain attack) | cast / hit | "glob arc and splash" |
| ch_undertow | Undertow pull (still a PROBE in Boss Fights) | hit | "water-drag streak"; needed only if the move survives the harness |
| Spreading Fire ember tile | The Fall's twist: the Arsenal Keeper's ember bands at rounds 1, 4 and 7 (drain tiles; the Burning Deck hazard is removed, Boss Fights §8, RUL-2026-10-30-060) | STATIC or loop | not specified. **Uncertain:** a distinct ember look, so embers are not misread as a heavy mark that resolves next turn |

### H4. UNCERTAIN (move exists, no animation named)

- **Steady the Helm** (the Captain's transition jutsu, RUL-2026-10-28-032/-045): no flourish specified; it shares a turn
  with the first mark and the Gunwale.
- **Mending Seal** ("soft seal glow"), **Stolen Form** ("mirror flicker"), **Extermination Order** ("crimson sigil"):
  named looks with no ids in the asset list.
- **The Last Directive blaze** (cc_last_directive, "crown and every armour crystal blaze white-cyan"): `crown_aura` may
  serve, or a brighter variant is wanted.
- **Shell Wall** (Sentinel barrier): may share the Gunwale sprite.

---

## I. Pet art: the Little Horror

Pet art is **generated per owner** by the engine from the species' `artDirection` and `rankConcepts` (10 ranks; loot
tables §5b). The species record has no image field (`fable/pet-species-builder` fixture). Nothing is drawn or uploaded.

| Asset | Status | Note |
|---|---|---|
| `artDirection` text | EXISTS (text) | `SKYGLASS_PETS.md`: "small, oddly cute rot-and-skyglass creature, the Core's bad copy of the ship's mascot" |
| `rankConcepts` (10 entries) | **NEEDS TEXT** | the doc gives a two-point arc ("oddly loyal blob with one tooth too many → towering skyglass rot-beast, still loyal"); ten concepts must be written. Writing work, not an art session |
| The Little Horror's Jar icon | NEEDS ART | D3 |
| Little Maw jutsu icon | NEEDS ART | F |
| Little Maw animation | reuse `anim_maw_v1.webp` | H2 (upload once, shared) |

The Deck Gull, Bilge Rat, Lantern Moth and Ship's Cat are cut (N).

---

## J. Quest icons (`quest.image`, a raw URL rendered as an ICON)

House convention: a chart run's quest icon is its chart's icon (push/265, 266, 270); Crownhold's is the Crowned
Captain's sprite. So the quest icons need **no art of their own**; they depend on D.

| Quest | Icon | Status |
|---|---|---|
| Drowned Foundry, Quarantined Archive, Captain's Watch | their chart icons | EXISTS LIVE |
| The Buried Cache | the Foundry chart icon (placeholder) | swap to `icon-chart-buried-cache.webp` when D2 lands (not in the push/275 rows) |
| Crownhold | the Crowned Captain sprite | EXISTS LIVE |
| The Low Tide Run, The Night Watch, The Sealed Reliquary, The Fall | Tide Chart, Watch Roster, Reliquary Seal, Last Heading | waits on D3 (harness specs carry the default placeholder) |
| The Rotted Reliquary, The Burning Heading | the two recolours | waits on D4 |
| The Haul, 6 quests | the page icons | waits on D3/D4 |
| Steeping, 2 special quests | never listed, started by an item | none needed |
| Wreck Sighted | **UNCERTAIN**: no chart of its own; the Tide Chart it grants fits |
| Walked Every Deck | **UNCERTAIN**: the Crownbreaker variant token or the badge fits |
| Proving Ground (hidden test) | none needed |

---

## K. Dungeon and Wreck assets

| Asset | Status | Evidence |
|---|---|---|
| Battle background (both Wreck versions) | NOT NEEDED | `background` is a closed `COMBAT_BIOMES` enum; both use `dessert` (RUL-2026-10-28-027). Custom tilesets are deferred and need an upstream change |
| Battle background (quest battles) | NOT NEEDED | quest battles take the player's sector biome (RUL-2026-10-28-027 item 3) |
| Per-floor scene art | NOT NEEDED (impossible) | dungeons have no per-floor scenes or dialogs (Dungeon doc; TEXT §6.1; RUL-2026-10-29-057 item 4) |
| Wreck entrance structure ("Skyglass Wreck", beached) | EXISTS LIVE | `structureAssetId` `gAsRCVBGRplS31wOYckh7` (push/263, verified); source `art/ghost_ship_skyglass/structure/` |
| Easy (level 45+) Wreck entrance | no new art | its dungeon record is built in push/319; it can point at the same structure asset |

---

## L. Everything else

### L1. Tier seal colours (RUL-2026-10-28-028 item 4, with the RUL-2026-10-29-058 tiers)

| Rarity | Seal | Charts (RUL-058) |
|---|---|---|
| Common | plain | Tide Chart, Watch Roster |
| Rare | cyan | Buried Cache, Drowned Foundry, Quarantined Archive, Captain's Watch |
| Epic | gold | Reliquary Seal, The Last Heading |
| Legendary | rot-green (ruled for tainted charts) | Rotted Reliquary Seal, Rotted Heading; also the Lantern and the six Haul pages |

"Chests take their tier the same way." **Uncertain:**
- RUL-058 moved the Lantern and the Haul pages into Legendary, but rot-green was ruled for the *tainted* charts. Does the
  Lantern (live icon, cyan beacon) need a rot-green seal, and do the Haul pages?
- The live Archive and Watch charts were drawn as EPIC (TEXT §8). Their seals have not been checked here against cyan.
- Applying seal colours to chests would touch live chest icons (Coffer, Treasury, Inro, Strongbox): a redraw that
  RUL-2026-10-28-007 discourages. The new chest icons (Galley Stores, Crown's Hoard) can follow it from the start.

### L2. Other items checked

- **Salvager portrait:** B.
- **Crownhold badge:** G (the Crownbreaker).
- **Forbidden cache tier:** a text colour (`#ef4444`) only; no art.
- **Sound:** the 16 existing SFX only (RUL-2026-10-28-028 item 1); no audio assets.
- **Map pins (`objectives[].image`):** none. Steeping lost its map-location deliver step (RUL-2026-10-29-055), and the
  runs start from the Battle Arena.
- **Ghost Ship quest icon** (`quest_icon_ghost_ship_skyglass.webp`, live): belongs to the retiring quests; unused.

---

## N. Not needed: cut or superseded by ruling

| Asset(s) | Ruling |
|---|---|
| 4 cut pets (Deck Gull, Bilge Rat, Lantern Moth, Ship's Cat): no species art text, no jars, no signature icons | RUL-2026-10-29-047 |
| The Echo Jar (five-pet jar) | RUL-2026-10-29-047 (the Skyglass Token takes its slots, RUL-2026-10-29-048) |
| Officer's Pill Case | RUL-2026-10-29-042 (never built) |
| Quartermaster's Kit | RUL-2026-10-29-042 (never built) |
| Titles (Relief of the Watch, Who Relieved the Captain, Keeper of Echoes, Walked Out of the Fire, Crownbreaker title) | RUL-2026-10-29-041 (titles have no image field anyway) |
| Trophies as items (the Warden's Maul / Ladle, the Wayfinder's Compass) | RUL-2026-10-29-041; trophies return as variant tokens (RUL-2026-10-29-047), E and D3 |
| 6 Rot-Sealed Pages and their steeped quests | RUL-2026-10-29-056 |
| Armory Requisition (item and its Special quest; live icon and pixel redraw #59) | RUL-2026-10-28-016 |
| Wave, Ikazuchi, Stonefall and Zephyrfang Tool Pouches (live icons; redraws #51-#54) | RUL-2026-10-28-003 (one Elemental Tool Pouch) |
| Pixel redraws of live icons, batch #49-#65 (Coffer, Katon pouch, three charts, Lantern, Requisition, Crown, Fragment, Crystal, Filament, Katana, Serum, and the four pouches above) | RUL-2026-10-28-007 ("I don't want to regenerate pre-existing art"). This reverses the 2026-10-25 redraw plan in the batch handoff |
| Skyglass scene redraws, batch #66-#79 (14) | RUL-2026-10-28-007; see A4 for the new-location caveat |
| Arakane avatar (live upload `fGSVwTtK8TwnOeZ7wXphI`) | RUL-2026-10-28-003/-007 (retired; the Crowned Captain keeps the crew sprite) |
| Crownbreaker badge v1 | RUL-2026-10-28-007 (v2 replaces it) |
| Telegraph strips `anim_tg_{heavy,control,linger,safe}_v2.webp` | superseded by the v3 tile + glint pairs (push/320) |
| Separate strips for ch_collapse, ch_rupture, fw_pour, st_tide, cc_shardstorm, dt_linger | covered by the shared library blasts and pool (H1; Boss Fights §5a) |
| Per-boss window strips (fw_cracked, st_exposed, sw_lowered) | one shared window tile (RUL-2026-10-28-028 item 6), `anim_exposed_v1.webp` |
| A "Burning Deck" hazard avatar | RUL-2026-10-28-027 item 4, RUL-2026-10-29-057 item 5 (the Arsenal Keeper's echo is the fire source) |
| The Skyglass Reliquary, the Mystery Chest and the old Ghost Ship chests | RUL-2026-10-24-024 (retired relics) |
| "Test Variant" generic token | hidden by the director, 2026-10-30 (push/327); not Skyglass art |
| Custom battle tilesets | RUL-2026-10-28-027 (deferred; engine enum) |

The 2026-10-30 decisions (push/326-327) bind the six live token variants to the Lion Token and hide "Test Variant". They
change no art; they make the Skyglass Token's art and variants safe to ship without unlocking older variants.

---

## Summary

Counts are images to make or upload. UNCERTAIN items are excluded from the counts and listed below.

| Category | NEEDS ART | REDRAW / RECOLOUR | IN REPO, NOT UPLOADED | EXISTS LIVE | NOT NEEDED |
|---|---|---|---|---|---|
| A. Scene backgrounds | 19 (Crownhold) | 0 | 0 | 10 | 14 |
| B. Scene characters | 1 (salvager) | 0 | 0 | 4 | — |
| C. AI avatars | 8 (Crownhold) | 1 (Foundry Warden) | 11 (Crownhold) | 12 crew (cover every Skyglass AI incl. the Crowned Captain) | 1 (Arakane) |
| D. Item icons | 19 (Tide, Roster, Reliquary Seal, Last Heading, Core Rot, Jar, Galley Stores, Skyglass Token, Crown's Hoard, 7 variant tokens, 2 Haul page bases, Countermand) | 7 (2 tainted, 4 Haul pages, neutral pouch) | 4 (push/275) | 22 | 30+ (§N) |
| E. Variant skins | 19 (12 Skyglass + 7 boss) | 0 | 0 | 0 | — |
| F. Jutsu icons | 4 (Lastlight, Little Maw; Last Directive, Extermination Order) | 0 | 0 | 0 | — |
| G. Badge | 0 | 0 | 1 (Crownbreaker v2) | 0 | 1 (v1) |
| H. Animations / FX | 9 | 0 | 15 | 10 | 4 strips + 9 design ids covered |
| I. Pet | 0 images (10 rank concepts to write) | 0 | 0 | — | 4 pets |
| J. Quest icons | 0 (reuse the chart icons) | 0 | 0 | 4 | — |
| K. Dungeon / Wreck | 0 | 0 | 0 | 1 (structure) | biome, tiles, floor scenes |
| **Total** | **79** | **8** | **31** | — | — |

### Suggested session order

1. **Uploads first, no generation (31 files, 2-3 manifests).** Run push/275 (four item icons) after checking the Buried
   Cache seal colour, and add the Buried Cache quest image. The director creates the Crownbreaker badge with the v2 icon.
   Build the avatar edits for the 11 finished Crownhold avatars. Create the 15 boss FX strips hidden, preview them in the
   Proving Ground, then unhide. These cost no art time and remove most placeholders.
2. **Item icons, charts and reagents (6 + 6 derived).** Tide Chart, Watch Roster, Reliquary Seal, The Last Heading, then
   the two tainted recolours; Core Rot; the Ledger Page and Stores Manifest bases, then their four recolours. Every new
   run's item and quest icon depends on this set, so it is release-critical. One shared chart family, seals by tier (L1).
3. **Item icons, rewards (13).** Skyglass Token, the 7 variant tokens (decide one base vs seven first), the Little
   Horror's Jar, Galley Stores, Crown's Hoard; then the neutral Elemental pouch (if approved) and Countermand.
4. **Variants (19).** One weapon per session with its live icon as the subject reference; the boss variants after the
   Skyglass set, so the pairs on shared bases can be compared side by side.
5. **Jutsu icons (2 + 2).** Lastlight and Little Maw (player-facing); Last Directive and Extermination Order if time
   allows.
6. **Animations (9).** The violet blast and cp_command first (every Captain fight and the Archive use them), then
   cc_phase_shift, cp_gunwale, ch_enrage, cc_hexweave, the ember tile, ch_bile_spit, and ch_undertow only if the move
   survives the harness. Key art in fresh sessions, then `boss_fx.py`.
7. **Portrait (1).** The Wreck Sighted salvager (the intro quest is public and cannot ship without one).
8. **Avatars (8 + 1).** The remaining Crownhold regulars; the Foundry Warden after the director rules on his redo.
9. **Backgrounds (19).** The Crownhold scenes, largest session, lowest risk: the placeholders work.

Writing task alongside: the Little Horror's ten `rankConcepts`.

### Top uncertainties (director decisions)

1. **RUL-2026-10-28-007's reach.** Read here as cancelling the 17 pixel redraws (#49-#65) and the 14 scene redraws
   (#66-#79). The four Foundry rooms and the three-coves shore are new locations; revive them or not?
2. **Variant token icons:** seven distinct icons, or one token base with seven motifs?
3. **Haul page icons:** six, or two (one per profession)?
4. **Seal colours for the Lantern and the Haul pages** (Legendary, but rot-green was ruled for tainted charts), and
   whether existing live chart and chest icons must be brought into the tier scheme.
5. **Crown's Hoard and Little Maw** have no art entry in any design doc; both are player-facing and would ship with
   placeholders.
6. **AI-only jutsu icons** (about 37): keep the engine default, or a small shared glyph family?
7. **Scenes for Wreck Sighted, The Haul and steeping:** reuse (assumed: `cache_site`, `hold` / `lower_hull`, `hold`) or new.
8. **Foundry Warden avatar:** upload the repo version, redo it (RUL-2026-10-26-002 queue), or keep the Arsenal Keeper
   sprite.
9. **Crownhold scenes:** 19 (batch) or 6 (package shot list); and whether they are needed for release at all.
10. **Animations without an id** (Steady the Helm, Mending Seal, Stolen Form, the Last Directive blaze, the Shell Wall)
    and whether the violet blast reuses `chain_wrap` / `command_absolute`.
