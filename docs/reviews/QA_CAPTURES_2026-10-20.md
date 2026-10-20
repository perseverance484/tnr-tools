# Content QA from repository captures — 2026-10-20

**Status:** review-only evidence. Built from the newest captured record per id across `harvests/inbox/*.json`
at `main@02a288e` (jutsu 870, quests 392, AI profiles 508, items 44, assets 40, bloodlines 29; captured
2026-09-13..2026-10-20). **Not live state.** Zero live-game requests were made. Item/asset visibility
outside the 44 captured items comes from the August seed index and may be stale. Every finding should be
re-confirmed against a fresh capture or the live-QA pass before any content change. Balance, reward,
rarity and publishing calls remain user-owned (CLAUDE.md §10).

## Top priorities (confirm live first)

1. **Damage blow-up risk:** Magma Slayer `98Qji30as-AHzsAbke5Z_`, Eruption Strike `dUyMUmOqPxBQ6u0Md6tR5` — formula damage/pierce without `generalTypes` (law 4).
2. **Bosses with no equipped jutsu** in visible quests: Akaibako, Byakuho, Kinmokuzai, Sin of Greed (Prime), Disciple of Sotek, Dojigiri (attack jutsu off).
3. **Starter chain may be stuck:** Kuroganekai GENIN `iUnQO8Fek3yJ-tL4Djv99` ends on a battle with no `win_quest`; same for both Rituals of Sotek.
4. **Battle→battle chains skip fights:** Kuroganekai CHUNIN, Subaku Demon Castle.
5. **Bloodthorn Cache** `OIw9FjNd-PXnSVzMtbclP` loot contains literal `[PILL_PACK_ID]`; rewarded by 7 visible quests.
6. **Endless Night Chest** (empty loot table) droppable in visible Marrow Vaults / Stormcourt.
7. **Publishing state:** Ghost Ship quests visible (and past end date) while rewarding unapproved Skyglass items; Mystery Chest edited 2026-10-13 to drop the "exclusive" Reliquary; Stormcourt visible though active-context says hidden.
8. **Visible test/placeholder content:** Draco test (OHKO, cd 0), Sticky Fingers (rob 100%, cd 0), Salt Gate Phantom staff test quest, "- Placeholder" AIs in Emergency Hunt: Godstorm, ~15 test items, 28 "New jutsu description".
9. **Hiding Water Technique** `5pr6XcEuVurUSFgl1S8Ay` gives its damage reduction to the opponent.
10. **Known fixes staged but never run:** `push/131` (Stormrender scaling), `push/33` (Copies, Not Thefts menus).

---

### Quests QA (captures 2026-10-05..13; not live)

Scope: 392 captured quests (245 visible, 147 hidden). Uncaptured 8 index rows are absent_since 2026-08-28 missions + 3 "New Quest" shells. Rules: references/quest.md, ENGINE_LAWS. Item hidden flags mostly from the August seed (may be stale); no badge catalog. Scripts: scratchpad/qa/work/.

### Bugs that break play (visible)
- B1 Battle→battle chains with no dialog (quest.md §3.7: all but one resolve without a fight): Kuroganekai: The Order of Black Steel CHUNIN `iQ5tqJaUKSvqbOybqVVDy` (daily; 5 chained battles; successDescription null); Subaku Demon Castle `Br7u84Gq7orlEpu0yqy1A` (floors 1–3 chain 3–4 battles each, floor-1 battles pay ryo/tokens/prestige each); Kuroganekai GENIN `kGeei→T0PZt`. Fix: dialog before every start_battle.
- B2 Kuroganekai GENIN `iUnQO8Fek3yJ-tL4Djv99` ends on battle `T0PZt`: no next, no fail route, no win_quest (§3.1, law 86). Gates Genin Trials 9: Debrief `jYyTQ5Ead2o3i5kzFSH2m` → Blacksteel Contract: Cleanup Detail `FvcbW7aLiGcJYT5MeMWb7`, and Kuroganekai CHUNIN. Starter chain may be stuck (needs check). Fix: battle → win_quest; fail → reset to dialog `Ccr9p`.
- B3 Ritual of Sotek `ANmue35P1QHVimRagpX3p` and Ritual of Sotek - Lesser `19KJYjkIT7GPP3LIvZcd7` end on battle `6iLxG` with no win_quest (needs check). Full pays 500k ryo + 5k tokens/prestige/clan points once. Empty dialogs `M3kdY`, `g9tC9`, `c3-3O`; "Go neeext", "stoped".
- B4 Skychain Monastery `M85vPxofZIVijLpspm7Uu`: promises Feint Charm drop; reward slot `{"ids":[],"number":20}`. Fix ids → `2LdMc6cJdw7oFC0V-xGiI`.
- B5 Dragon quests reuse Azir's dialog `Zx2Br` ("Sector 66 (10,10)"); real fights in 34 (Balista `3XSo3-RrLIqG1o0Ng-9DL`), 72 (Aery `A-MwXj8Ik7qcMSpwv70ag`), 35 (Baby Diamond Spotted `6bZzBUYiIZGvthNUIezDp`), 24 (The Eggs have Hatched `4j9W0N4Hba24NFffn3ToX`, whose description says 25 (15,18)). Also "Grasslands, . Currently", "Sands.Sector".
- B6 Vulcan The Infernal raid `hPPphfPQyVpFKpno6A61o` shows Ravena's description/success text.
- B7 Salt Gate Phantom `nwVJG9bsllGo7DefKM2ic`: public staff test quest; prerequisite `viNcVFLyaFgP1ua_YcbkW` doesn't exist. Hide/delete.
- B8 Retries reset onto the battle node (law 88): `rs_f2 → f2` in The Tenth Name `8ndqsf6RBZ88q3pfyZQQh`, The Empty Contract `9kzvd414kRRXauKSXsGIq`, The Waystation `ATV6Fs3XFqOf7wch99qDW`, Old Ghost `KmGPDnZnGOCvATQqA5LI8`, Chalk and Corner `Sx_NfWziba6NYOEsfXrS5`, The Long Winter `WIsqHEoo4c-ToRaV5_cZj`, Three Rounds `fBQNC1wFqTPYp7reiK79T`, The Loud Way `ilYoJqbk--np9OSqT9lGx`, Protection `otFtGNvBFn8ZVGlda7UOH`, Nothing to Report `s7Lnjsv-9Fvo4_YEzq-3w`; The Chunin Exams `iB3mdNvAZfBWVhsMEVBBl` (`pOY8P → UQyD3`). Needs live check.

### Content defects
1. The Path of X (Hard) ×6 (`rstId7S5I0Aoi6-lO00kr`, `hRl3SHwOnA_jF1c-N6oOy`, `TWmUEAPEVWbGIuwee2dTy`, `gXSl56_LkI2sk7AvAwMpD`, `z3ej62ONViP-vZ6q48FX1`, `bfBq9JxokqZz4McHul162`): "Keystone not available" vs success "Keystone attained."; "strength,and", "it's defense"; Greed (Hard) fight on edge tile (5,1).
2. Echoes in the Gust I–V (`lvk_8pyOASQg3LGdDb2Gz`, `cvFbswdbkpJblTrv--xCn`, `HHmJrZpTmip_70_No2f6c`, `gdw5q0UKSbX8i_vn1r7Ij`, `hmrHzNi_2gcPAARGFWm3w`) identical text.
3. Shiverthorn `ziucpd6c2NALT3_Hfa0Rj` says "Wraithbloom", rewards Shiverthorn.
4. Daily Arena Run `t44i7_DO7vaoejZML8W2r` uses creature-hunt blurb.
5. Round up the Escape Animals `hzUpMC9nimPoWz3SPdhtY`: empty reward ids; scene characters `bMhLVNPMyMRB-1HUdQUXa`, `oI5jt1XBHUeNd3pgCO3SW` unresolved; 4 fights no fail route; "GENIN 03" twice; "Sechi's Zoo's", bare "Success".
6. It's Pizza Time `CaoXAT7AjuwAir5GrEHjg`: move objective `oxAZT` at (0,0) sector 221; collect `aKKB5` on edge (21,25); Pizza Sauce/Cheese/Toppings (`PRc2glrHugsdNqZEKI6yt`, `HWmro5lrtllnCaHOhJI6k`, `M3UdoLW5WFx3Wb1aCqoar`) hidden (don't show in inventory, H23); duplicated dialog.
7. Getting Started `eYDVpL63vPhK3lywMexdv`: description "... empty office"; "That concludes, this one."; requires unknown village `XN9oEb5tKAv` (also The Broken Gate `An3HqyV6lhWaGeVCkwp8_`). Needs check.
8. Blood of the Tiger, The Dragon's Wrath `DOiYuFgUVCIKc7ecpLtnD`: same badge granted twice.
9. Forbidden Jutsu Trial: Momo `2vZ5uJdzYZXPJ_g37KseQ`: null success text; 15 fights no fail route; one objective 10,001 ryo; total 2.15M ryo.
10. Hidden items from visible quests (seed flags): Subaku Demon Armor `pvSUaWgUeGi7e81tYwxpW`; Mizu No Odori Sample `iYNVCnkkLg0WAm_oRXdaV` (Marrow Vaults `2yvE9PUQqlD8lbYNfgX-b`, Stormcourt `OSADdXqostbyVliCxWk6k`, The Nameless Thorn `qn36dRZfTnru7oSgjDElO`); Vital plasma samples `Y1GO3wJjnWlXLi6K7ZMeV` (Nameless Thorn, Marrow's Bloodshed `tM9iwD_iBY3-7USNDlcGa`).
11. Introduction To Farming `LXwiSxro5WNHHzFGjmoHf`: seed/fertilizer ids resolve nowhere (needs check).
12. Kill the Creator `g2ilVOzFys21wkEHwfTeE`: opponent player account `user_2SBp5J5epcr9DwIiRJX5lg7Scgp` at sector 0 (0,0); push/92 lookup unrun; "you probably annoying me".
13. 12 visible quests with empty/null success text (Kaeruun's Pyramid, Howling Hills, Kuroganekai CHUNIN, Momo, Crimson Masquerade, Medical Ninja, Arena Champion, Genin Life, 3× Relic: Shūren no Yaiba, Thalymr) — next edit will fail schema.
14. Empty battle descriptions: Subaku (14), Howling Hills (10), Kaeruun's Pyramid (5), both Rituals, both Kuroganekai, Engines of Ruin.
15. 27 visible hunting quests: win_encounter_at_location with empty image → no map pin (law 52).
16. 15 visible hunting quests: nextObjectiveId to nonexistent ids (e.g. `2E19R→JnIkf`) — harmless in play, blocks edits.
17. 34 visible quests with fights lacking fail routes (§3.2) — mostly legacy, needs check.
18. Archive Settles Up: Astral Ascendant `_S3fhIPpNV6jJpPF0czO6`: no end date; siblings ended Aug 23–31.
19. 9 visible past end date: Crimson Masquerade, Crimson Harvest, Borrowed Awakening ×2, Archive Settles Up ×3 (August); Ghost Ship (Gather) `6Ri-W5TtUrEMWpyYlnf_F`, (Hunt) `HckXVOf-qk6ESU9t5rxLh` (2026-10-19).
20. Starter level windows (needs check): The Chunin Exams only L27–30; Road to Genin L1–20; Getting Started L1–10 — out-levelled players may be unable to rank up.

### Low-quality content (visible)
- Xerath the Infernal Talon - `KJaVpLJiUXQOLTmDjM7Z5`: description and success = "The Infernal Talon".
- 10 visible raids: zero rewards, boss health 0, no end date (needs check); "Larry The Fish has return" `r9tpM8s1Nt4dwKE_mL3r-`.
- Hunting blurbs: "the follow creatures" ×13, "available to hunted", "Kaijoka" vs Kajioka, "creatures has started" (Emergency Hunt: Godstorm), Warped Taka "Secret A Rank" but D; questRank one letter below name; Amir-The Hoarder breaks pattern.
- Shinobi Fundamentals ×4: "<p>Sharpen your Mind</p>".
- The Path to Kitsune `guSLlHTobmxnOqacGIblJ`: garbled description, every objective "Fight and win", 1M ryo for 4 fights (event median 50k; your call).
- Missing apostrophes: Akasumis/Akikazes/Hyorins/Shirohanas Broken Gate.
- Bully the weak: "Successfully kill the elderly…".
- Typos: "switfly" (Infiltrate the Underworld `4UoMSPmAyifHeqK58DJ_d`), "a thing or too" (Skill Issue: The Chief `1hMJgpCBFO-iHdx8SbZcB`), "Moonviel" (Moonveil Moss `4yAxTBSxv0eyTUlMSZ_UA`), "Celestial Thristle", "complete the objective earn 1 silver" (Blood for Silver `fyjd5WGEh5outjht89UfM`).
- Copies, Not Thefts `d-94cxrGW91o1SJCr9rsq` generic "won the battle"; choices converge (also Kuroganekai GENIN ×3, "Attempt to Flee" does nothing).
- Genin Trials 8 `KP0__fXg2i6pLOQ95yTWX` typed event in starter chain; pays 100 exp / 2.5k ryo vs 200–500 exp for 1–7.

### Polish
- 22 visible names with trailing/double spaces or dangling " -".
- 21 em-dash dialog lines in 9 visible quests (house style).
- Rank letters vs difficulty (Kaeruun's Pyramid D at L70; Skill Issue D at L80).
- Dragon descriptions use HTML headings + emoji.
- Hidden Totem/Supplies text: "to to", "for for", "Bravely Bravely… Away Away".

### Hidden quests
Broken if published:
- Story: The Ember Ledger `UYlTqs-BzK-9JFmSVnP9l`: ~200 nodes with names in sceneBackground.
- The Shattered Sakura Part 2 `KbJe4-VJagO_zrCX2wN1P`: max L12 but Part 1 `Y1-3FAnTTZevvMQ-aZL-0` needs L21; Part 1 reset with no target.
- Goah Way: Forest Trail `qaMzIecpcr6MYls1qla72`: start after end; unknown village.
- A Starry Night `1qxKCQhdBA4cqORAhMJ5F`: battle with no opponents.
- Test/scaffold: Kaeruun (TESTING TAILED BEAST), Pyrrakai (Two tails test), Rebase Canary Gauntlet W1, Dusk Workspace, Christmas Present Selection (DO NOT TAKE).
- (0,0)/sector-0 objectives: Mermaid Sighting (+3 resets onto battles), Beach Day, Sad Puppy Revenge, Totem of Tsukuyomi - Story, Iron Ascent.
- Path of Crimson I–III: 9 collect ids, 1 reward, 1 AI unresolved.
- 8 old missions use unresolved AIs `E7zjSGym1Bct60eQVnhCK` / `Ggt66lVPZsHTZ0DCnC_kn`.
- Battle→battle chains: The Last Shadow I and III, The Ascension Ceremony, Under the Pale Loom, VEILNIGHT, The Drowned Fleet.
Look ready: One White Ear `STAQqoCbpb6I2W39syED_`, Blacksteel Tides `0LcoGMpeBcXVu8p3ISOK7`, Ren of Wake Island I–III (together), Eclipse Mandate I–V (together; choices converge), Shadows in the Updraft `t-08THKXHdTq1r-46PxSr`.
Blocked by missing scene characters: Resort in Need `xG0_Jq-amzhFgcLy8BVjw`, The Concord Table `v--6JyIMQQ9fNNs6C6Q0j`, The Wind Beneath the Ruins `_53c9Ms81QquXXAi8I_dj`, One Perfect Crop `CZIZoHDAOWjxDtVaQwr6V` (empty description).

Counts (total/visible): battle chains 3/3; end on battle w/o win_quest 3/3; resets onto battle 13/11; no fail route 86/34; no map pin 39/27; bad nextObjectiveId 15/15; unresolved refs 29/10; hidden items from visible quests 6; empty success text 23/12; visible past end date 9.

---

### Jutsu & bloodlines QA (from captures; not live)

Scope: 870 captured jutsu (615 visible non-AI), 1,472-name index, 29 bloodlines. Rules: ENGINE_LAWS (2, 4, 6, 77, 78), references/jutsu.md + balance.md, 45c/45g contracts, runtime laws R1–R55 (46b_DATA_tag_runtime.json). Tags: [verified] data shows it; [law] engine law predicts it; [needs check]. Scripts: scratchpad/qa_work/.

### Bugs that break play
- B1 Magma Slayer `98Qji30as-AHzsAbke5Z_` (BLOODLINE/B, visible): formula damage has statTypes but no generalTypes → law 4 damage blow-up (trillions, seen live). Fix generalTypes ["Highest"]. [law]
- B2 Eruption Strike `dUyMUmOqPxBQ6u0Md6tR5` (BLOODLINE/B, AoE): same gap on formula pierce. [law]
- B3 Hidden: Yeti's Soul `LfOvBN_hn5oYJtQfR25ob`, Elemental Combo Test 1 `MApIOjZE6FWkXlJiblf3a` — formula damage with neither statTypes nor generalTypes. Fix before unhide/AI equip.
- B4 Water Release: Hiding Water Technique `5pr6XcEuVurUSFgl1S8Ay`: targets OTHER_USER; 10% damage-reduction row is INHERIT → buffs opponent. Fix target SELF. [verified]
- B5 Storm's Lullaby `Ac1nbz3RUrPCCWmiOl7Jr`: OTHER_USER with cleanse + 800 shield, both INHERIT + friendlyFire FRIENDLY; text says disorients enemies → likely no-op. [needs check]
- B6 Retribution `ZnXkvxDfvw6SNtpVj7yhe`: absorb has no rounds (R28 → likely never fires); promised ninjutsu boost absent. [needs check]
- B7 Corrupting Miasma `sjwQXKYglLj0xLnQ2V9iI` (SPECIAL/A): text = poison cloud; only effect +10% caster stats, cooldown 0. [verified]
- B8 FBA `C1S_SGYNao5gc85A7t-OF` (visible): no seal despite text; drain rounds 1 never ticks (R48); "HKD Copy" battle text, 0.05 costs, cd 0.
- B9 Sticky Fingers `wvmEuCP9hyd19tTgIKLE9` (LOYALTY/D, visible): rob 100%, cd 0, placeholder costs/text. Balance call; needs cooldown, costs, text.
- B10 Draco test `EoPhRA0116ycHlkSo1L2J` (SPECIAL/H, visible): OHKO power 100, ALL, cd 0, from STUDENT. Hide.
- B11 Final Boss Phase 2 `oFtgWmKCgMq9zLqe6Nt3j` (visible): test-named boss jutsu. Hide if boss-only.
- B12 Amaterasu's Renewal `-b6rDhdrIDL5Ggs6_6xET`: battle text has invalid token `%Amaterasu`. [verified]
- Likely dead static damage rows (residualModifier 0, rounds 2): Torturing Flame Coil `XlgQwf4VfQ76OSP-8qHun`, Infernal Combo `Ki9gt7RZI4pGb-ySjG6Zq`, Flame Burst Punch `vNqDxhiAFx9oUQ2vMBOpa`, Drowning Mire `VmZzkyfPswbJLXvuB-mcV`. Either 0 damage or unscaled large damage — confirm tags.ts:1387-1395. [needs check]

### Balance outliers (user-owned decisions)
- L1 A-rank bloodline increasemastery: 11 lines +50k ×4; 7 lines +1,000,000 ×1 (Vaporia `f7IgtcsLqomqmmBgAYS1O`, Crystal Essence `ssevlOGQ4JjPn2sHZtq0c`, Heavenly Sonata `clh4d6q6s000atb0h0qdqdh1z`, Houkyuken `ALoGrHuBY5Ml9bJG_DILe`, Teno Yuki `clh4d6qjs000gtb0hr357gjvv`, Itojinsei `j4_9ypNqYq8Ifbqf-9D2r`, Shadow Weaver `d0WYPbbsVx7Y_i0fddwxc`); Kyuko-sei `Y10fxyLR39IBJ3ICkAdEp` +100k; S rank +75k ×4.
- L2 H-rank lines (Night Parade `r_99Xg8SIOYw2awCMSR7e`, Tetsugan `T-MyR4yQ1_aVbaJDLoI07`, Sands of Time `yzbSbZ5rqRVIjiwN-farx`, Godstorm Eclipse `szai-IgtB7PLubojIIlh-`) only +25% damage given; A gets three passives. [needs check: bloodright may compensate]
- L3 AP outside 40/60 on 20 visible jutsu: 20-AP 30% damage buffs (Infernal Ascension `1Utdp_1sdXw7CUOB_EXhY`, Tides of Sovereignty `SQuwOilXd6w-v0HHKy7yn`, Tectonic Ascendancy `VL85zkB3uifqpF2T8OEnE`, Fan Dance `g7nr36h9VVpRKtHicMl2L`, Lightning Cloak `rjV6z8ygicPTp1TZ1ybrB`); 100 AP Energy drain `7idaA9dUXSWmILp1PbVkE`, Crippling Blade `z17S47TiSnNBgQMVkxsnH`; summons 70; Widow's bite damage at 20.
- L4 Damage at 40 AP: Hittakuri `RL9frAr3PJrbxVc-U8uqj` (damage + 15% debuff + rob), TGC, summontester.
- L5 Cooldown 0: Primordial Blight `Uu1J0ht_YiSNwUoPca5Jg`, Corrupting Miasma, Crep wall `XU0RiYC92ZeErHT6Q5-oX`, Corpse Jutsu `joE-MVdQImoa1804Ja8Y3` (heal 700, cost 2/2).
- L6 Thousand Strike `znPva-HIAz4EkyuKm2oh0` pierce 60 vs 30–48 peers.
- L7 D-rank cost-5 static 100 damage: Poisonous Senbon `H9XLJiU1YEro03QJ2mH8q`, Soul Shackles `clh4d6psu0004tb0hsa5cshh6`, Sonic Slash `clh4d6pxd0006tb0h4y1yudi5`.
- L8 Power 14–15 at 60 AP: Seven Heavenly Pillars, Cyclone Prison, Arcbound Vortex, Eroding Current, Drowning Mire, KGK: Flash Step.
- L9 Pool cost: B-rank 60 AP at 50 (Lightning Flash Step, Earth Release: Boulder Crush, Tidal Crash, Wind Release: Whirlwind Demise); A-rank at 200 (Shrapnel Clone Barrage, Fireball); Black Crow D-rank 1000.
- L10 >3 tags: Reaper's Embrace, Crimson Impact, Lightning Release `XLrUa_lnAbiYPBwNjTufc`, Fire Release `jJfbQCH1--LjLDnQw-cL3`; 6 Forbidden.
- L11 Gating: Summon: Totem of Tsukuyomi `c6Wz7nyb27Tz9YkUpOHb3` STUDENT vs siblings JONIN; A-rank at CHUNIN (Iron Fist `Oi5pYxNaHa-5o737i5gAu`, Typhoon Tear `G9NyTKDVP4mCFzoZEzPmA`); C-rank at level 70 (Danse Macabre, Seimyaku, Severed Pulse) or 50 (4 more); D-rank bloodline at JONIN (Oni Hammer Swing, Possessing Yurei); S-rank EVENT from STUDENT (Moose Cleave, Moose Prime, Hogs gone Wild, Frictional force).

### Content defects
- C1 "New jutsu description" on 28 visible (49 captured), incl. bloodline Phantom Slash `lXlcfj4ZrhX8mzkOgy0oI`, Crimson Thrust `oh9CmLX8nltc2WfrkvswH`, Shadow Pierce `J6HTCnlUw84zOyaf9xxmD`, Middle Guard Stance `r2QGirLcf1lpWvYCHS60g`, Equilibrium Guard Strike `OQqC5LhjVMFMmI_zoR9S7`, Vacuum Fan `QE05DhEhb09fhnC1573Vj`, Inner Peace `sav_H5tjyeHUIlGNPKC3h`; injected Voltari `uVRjiBKSVATMYxEqPZuFw`, Stardust `0_ip_8I2Dh_Ti2mYUcuAu`. 14 keep default battle text.
- C2 Truncated: Earth Release: Boulder Crush `Pvp1t3YrApYswT4xKodnP` ("he user…"), Pressure Damage `haRHBRJ7ifpnXApDOlSVk` ("his tornado…"), Windslicer Roundhouse `t7OF-sg2Z6tjjhwZAYZfd`, Quicksand Mirages `oEf8f1hEHz4a0to5YAACt`, Void Rend `_QfGq0SseWD11jHO23pr1` ("recov"), Harden Fist `C1SdH7N13naMHG3bKE07k` ("motio"), Tempest Slash `_6PY8GqUsMgH8D71ys9VQ`.
- C3 Text ≠ effects: Magma Slayer (says summon), Fist of 10 ,000 Volts (names "Thunderclap Strike"), Crippling Blade ("Crippling Strike"), Sonic Slash (says pierce), Danse Macabre (seal only affects bloodline, R18), + B6/B7/B8.
- C4 Name typos: Draconic Assasult `GfTFDG-XVTA051VDTdqSb`, Dust Dismanting `242qP5Yw-4Psxmgt7BjHy`, Fist of 10 ,000 Volts `JKgaTbuFTeNZjYOXrb49M`, Reapers Storm `XsFfE_DaNchPuXRcCWa7T`, AI "Titanboa" `Gvl__65z9lZRZtPZP_zQR` (Summoning: Titanoboa `ZeqpsECJ882inNKUu0t3d`), Judgement/Judgment split.
- C5 Text typos: cresent, Forbiden, fronnt, lazor, "wraps it selfs", striken, wiries, "opponents loves ones", leach, summoning's, "users" ×3.
- C6 Whitespace: "A  Frost Dot" `UKRwFavvgnJ6XlLT-PZn_`, "Shield  Dust" `ZBjzrZSzjWwz3rHR2-uq2`, "Crescent  Reaper Fang" `cjRErpuffG4GiwIU8OsCw`; 10 trailing incl. "Venomous Phobia. " `9oirFnLa0wejelNYpewq6`.
- C7 Duplicate "Singularity" `VDlEcF_uGVORTDrLSuujZ` / `7GGmPc5Sbp3JSeHGYgaJV` (both visible bloodline); visible "Unknown1–5"; near-dupes BEE 1KS/BEE1KS, Tempest's Whispers/Whisper, Tidal Crash/Crush.
- C8 Five SPECIAL copies on bloodline `cB2LWCWyLRHxgsbY0crJr` (Planetary Ruin, Surging Water Slicer, Voltaris, Grand Fire Annihilation, Greater Vacuum Bullet) duplicate Shiroi Youso's injected jutsu; nothing captured injects them. [needs check]
- C9 Unresolved bloodline ids: `Dqqw3zcIGDserD-qEE9QW` (Overloaded Impact, Chakra Overload, Chakra Cannon — visible), `cB2LWCWyLRHxgsbY0crJr`, `X2namEaqY0MfeeFJ3hGfj`, `0Uc2Nfgg08kqGm78QAwZ4`. Non-bloodline types carrying bloodlineId. [needs check: capture all bloodlines]
- C10 ~22 visible test/dev SPECIAL/LOYALTY (Draco test, Field Test, Elemental Combo Test/3, Sage Mode Test 2/3, Static Tag Test, summontester, Final Boss Phase 1–3, FBA, TFG, TGC, Momo3…); index shows 176 visible AI-type jutsu ("AI 20% Placeholder" `jvZKZf2_xYdQWUXHxtqzq`, "Impossible AI Jutsu #1", "human ai 1–5"). Hide; unequip → edit → re-equip for AI-equipped ones.
- C11 Visible but only via hidden quests: six "Summon: Totem of …"; 14 EVENT, 7 FORBIDDEN, ~40 SPECIAL with no captured source. [needs check]
- C12 Default image: Elemental Combo Test, Elemental Combo Test 3. Old hosts may 404: Lightning Blitz Strike (S3), Flash Pulse (uploadthing.com). [needs check]
- C13 Hidden, no effects: Stellar Flashfire, 5-jutsu Metal Release set.
- C14 Kyuko-sei damage-reduction row text "Adjust damage given by target".

### Low-quality content
- Bloodline lore: Sands of Time "Rank Reward Bloodline"; Tetsugan 51 chars, no traits (others 750–1,700).
- Short descriptions: Herald of the Apocalypse "A magnificent tale"; TFG "8 gates"; Summoning: Titanoboa "Summon the great Titanboa".
- Battle text: joke lines (Frictional force, Hogs gone Wild); 28 never name %user; Summoning: Momo "%target offers their blood".
- Shiroi Youso kit named "Lightning/Fire/Water/Earth Release".
- 142 descriptions without final punctuation; 6 start lowercase.

### Polish / informational
- 1,245/1,338 visible effect rows have "placeholder" descriptions. [needs check: player-visible?]
- 417 visible jutsu (515 rows) carry legacy statTypes/generalTypes on tags whose schema lacks them — strict update validation (law 2) will reject unchanged resends; strip on edit. [needs check: ignored → "Taijutsu-only" buffs apply to all?]
- 47 visible wound rows without generalTypes (no blow-up; validate.py warns).
- 515 visible jutsu with powerPerLevel > 0 (legacy); none passes 100 cap at L25.
- Static heals ×10 (R3), rounds ≥1 → heal only later rounds (Corpse Jutsu 700, Celestial Dew/Dark Pact 400).
- 20 bloodline jutsu with inline HTML colour; 124 leading/trailing whitespace; 26 double spaces.
- Tokens to confirm: %user_object, %user_reflexive, %target_object (Clone Technique), %user_subject, %targets, %weapon; 13 self-target jutsu use %target.
- Bloodline trait trailing commas/casing.
- Animations unverifiable (no animation assets captured; 238 ids); 9/23 SFX ids unknown; 79 rows use literal "hit".

Counts: 12 bugs + 4 likely-dead rows; 11 balance; 14 content defects; 28/49 "New jutsu description"; 7 truncated; ~22 visible test jutsu + 176 visible AI-type; 4 unresolved bloodline ids.

---

### AI enemies QA (from captures 2026-10-12..18; not live)

Coverage: 508 captured AI profiles, 39 rule sets (~9% of ~436), 392 quests, jutsu/item indexes. 29 indexed AIs uncaptured; 5 captured AIs not in index (Road Bandit, Harvest Boar, Wayward Blade, Jellyfish, Jelly Chakra Beast). Game source not in container: "only equipped jutsu used in combat" and "loot uses dropChancePerc" rest on documented laws (18/60, 69) — needs source check.

### Bugs that break play
1. Bosses in visible quests with their whole kit unequipped (basic attacks only):
   - Akaibako `x8WbnaeJe4fkH-vCi4itG`, Byakuho `KB4S6xvKDDhv4wDvMuQuJ`, Kinmokuzai `LIbrBQ9KR3AeHiIwZnGId` — 4/4 unequipped (S Rank Hunts)
   - Sin of Greed (Prime) `erDLuK6pzuU691_Kdl74d` — 5/5 unequipped (The Path of Greed, Hard); normal mode is equipped
   - Disciple of Sotek `uyFMFCdXQecgu8YaJZoC9` — 5/5 unequipped (Forbidden Jutsu Trial: Momo)
   - Dojigiri `7WY2QmiPnbWnir7RPS1X9` — only 2 self-buffs equipped, no attack jutsu
   - Fix: unequip → edit → re-equip, verify with getAi read
2. Player summons that bring a kitless AI: Hellfire Hound `-xF_-Uz5lF83yLGpQW2Z1` ("Summoning: Hell Hound"); Mr. Waddles 2.0 `a0FYTNLNsLO50Ltl9X-A5` (STUDENT, 0/2 equipped)
3. Unknown quest opponent ids (needs check): `RBW5KsIXmTGR710D2y2Y7` in Ghost Ship (Gather)/(Hunt) "Challenge the Sealwright"; `user_2SBp5J5epcr9DwIiRJX5lg7Scgp` in visible achievement "Kill the Creator"; 4 more in hidden quests. push/92_ai_unknown_id_reads.json has no committed result.
4. Skyglass Sentinel `3V_gdHYaclMB1gTyOPAbV`: 5 rules reference 6 jutsu it doesn't own (Ghostly…, Braced Stance). Needs check (rules capture predates profile capture by 20 min during the 2026-10-12 remap).

### Balance outliers
5. STUDENT-rank AIs clamped to 20k/stat (law 16) in player-facing quests: Fire Grunt # 2 `PdsZeCsshdcStNSl8YlVk` (L60, 114k→20k); Frost Warden `gqOxWqXElRszsLksj83zx` (daily); Howling Hills 6/10 opponents STUDENT; ~30 more in hidden quests/summons (e.g. 20 Black Maw L100).
6. KGK Rogue `gocAYWKP6NwO3YXFHfPV_` (L10 GENIN, unscaled) in 6 visible Blacksteel/Case Contract missions requiring L14–50.
7. Stat-budget outliers: Titanic Destruction `Mzl0Xd5NeBqjsDYV__YVx` 1.37×; Sin of Gluttony `MUIvP0kikNv01CeKnuT0k` 1.29× (other L60 Sins 0.95×); Kazehiko `user_2ue4TutSeewDxpR7CqT4IhC7b` 0.07×, 0 jutsu, unused.
- AI-only armour at 1% drop (Court Regalia, Ashen Regalia, AI Heavy Armor on 16 AIs) — possible law-69 count/percent trap (325/460 AI item rows at 1%). Needs check.
- Endless Night Chest unequipped on 6/15 Tower bosses — may drop nothing. Needs check.

### Content defects
8. Placeholder names in visible "Emergency Hunt: Godstorm": Warped Taka - Placeholder `kPCr_dLz14u5Ky1WhjRAb`, Tainted Kuma - Placeholder `2uclFUM9AeUEj2MlLY91n`, OctiKameá - Placeholder `Jn_yCpp75axp9BQUM4LzB`, Mōmoku Inoshishi - Placeholder `fUlYeOzHb8AJVD4pV5hxd`. Generic "CHUNIN 01–04" (The Path to Kitsune), "GENIN 01–03" (Poachers' Due, Round up the Escape Animals).
9. Placeholder jutsu on player-facing AIs: "AI 20% Placeholder" `jvZKZf2_xYdQWUXHxtqzq` (Subaku Prince); "Nisshoku new" `57tZ3QOnJyeW0cZu2Rca-` (Masked Chunin in The Chunin Exams; Kori no Seirei arena). ~20 Seven Sins jutsu with empty descriptions.
10. Arena: Yokai Thief/Devil/Marauder (L100 summon-flagged) and The Jester (L130) with no jutsu/items/rules; Amaterasu's Avatar L190 with 0 jutsu; L25–L80 ladder (13 AIs) carries only 1–2 generic jutsu.
- AI Heavy Armor unequipped on The Captain, Crowned Captain, Seal Charge, Core Canister.
- Mommy Shark's Baby Shark summon → missing AI `nmZZhX-YioQBTzbBGaycK`; both summon jutsu unequipped.
- Zero-jutsu AIs in visible quests: War Commander (Warpath), Syndicate Thief (Night Watch Shadow), Cave Goblin (Howling Hills).
- 62 AIs partly unequipped (e.g. Unkei no Kami 3/6).
- Duplicate names: 6 sets (Frost Sovereign ×3, Axel the Elf / Axel the Elf-, Dagger the Elf / "Dagger the Elf - ").
- isSummon mismatches: Titanboa, Lord Pengu summoned by visible jutsu but not flagged.
- Fire Grunt # 3 regen 1 vs siblings 60.

### Low-quality / polish
- ~25 squashed shorthand names (FalseAtt, RopeSab, UltChair, RunStool, MaskInfil…), mostly hidden quests.
- Jutsu typos: "Shocking Hammer FIst", "Cyrcle of undying flesh", "Aeldari Thurst".
- Odd gender values: DOOM, Good, Canine, Titanic Unknown, Summon, lowercase variants.
- 33 names with leading/trailing/double spaces.
- 7 "New AI - <id>" records (6 are 100-HP stat-10 L100 STUDENT).
- 72 default avatars, 5 none (none player-facing).
- HP desync: Ariel (37,750/7,550), Drakar of the Maw's Flame, Kazehiko.
- Seal Charge / Core Canister single rule is intentional.

Totals: 86 AIs with no equipped jutsu (61 own none; 25 all unequipped); 62 partly unequipped; ~44 under-ranked; 209 in visible quests.

---

### Items & assets QA (from captures + stale indexes; not live)

Visibility for the 44 full item records is captured; for the rest it comes from the stale 766-row index. Hidden scene assets in visible quests are NOT defects (law 16c: hidden assets still render).

### Bugs
- B-1 Bloodthorn Cache `OIw9FjNd-PXnSVzMtbclP` (visible): loot line `{"ids":["[PILL_PACK_ID]"],"number":20,"quantity":2}` — unresolved template token. Rewarded by 7 visible quests (Crimson Harvest, Skirmish, Sabotage Run, Decapitation Order, Warpath, Triage Under Fire, Hold the Line). Description "New item description". Fix: Pill Pack `XX8TLmUNJtqeiGM1T99tD`. Needs check: roll behaviour.
- B-2 Endless Night Chest `HLycjzUcVwKZenBWpd0V-` (hidden, empty loot table "[BALANCE: table empty pending Content Admin]", default image) carried by 15 AIs at dropChancePerc 1, incl. 5 in Marrow Vaults `2yvE9PUQqlD8lbYNfgX-b` and 5 in Stormcourt `OSADdXqostbyVliCxWk6k` (visible). Law 67 → can drop a chest that opens to nothing. Fix: 0% or fill table. Needs check: do hidden items drop.
- B-3 Stormrender `cLXXf8RJv5l9B_gGsYN2a`: elementaldamage has no statTypes/generalTypes (capture 2026-10-20). Known: docs/reviews/STORMRENDER_HIGHEST_SCALING_MANIFEST_GATE_20261020.md; push/131 staged, not run.
- B-4 Round up the Escape Animals `hzUpMC9nimPoWz3SPdhtY` (visible): scene characters `bMhLVNPMyMRB-1HUdQUXa`, `oI5jt1XBHUeNd3pgCO3SW` not in any index/harvest — probably deleted. Needs in-game check.
- B-5 Copies, Not Thefts `d-94cxrGW91o1SJCr9rsq` (visible): a1/a2 all choices → same node; f1 2 of 3 → f3. Validated fix push/33 (state/fix_copies_converging.md) never applied.

### Content defects
- C-1 Ghost Ship quests `6Ri-W5TtUrEMWpyYlnf_F`, `HckXVOf-qk6ESU9t5rxLh` visible (2026-10-13) but reward Skyglass Katana `ZSUdrzzgorepP4CQrBfEk` (pushed hidden 2026-10-12; 3% quest, 3% Crowned Captain) and Skyglass Reliquary `FVYuxw5E5b2lPOn3cbFfF` (100% secret ending; uncaptured). Publication not authorized (RUL-2026-10-10-001, RUL-2026-10-11-004; state/ghost_ship_skyglass_reward_decisions.md "Still open"). Fix: capture the 4 Skyglass items, then finish+unhide or re-hide quests.
- C-2 Mystery Chest `c5dUPtXmCedfKssqiwbpt` (visible) edited outside repo 2026-10-13: drops Reliquary 10% (designed exclusive) and itself 20%; description promises better Ornate odds but Ornate is 5% like others. Needs check.
- C-3 Bag of Prestige `llCOxrK200QbY2ON7uQ1m`: description "Item ", battle text copied from a contract item; grants 700k hunting/medical/gathering XP + 5 Seichi Silver, no prestige.
- C-4 "New item description" on Rusted Gatherer's Chest `toBESPaPaHI5vEFRjWi20`, Rusted Hunter's Chest `-v1OQ5QSsWbV-DcZadM0h`, Bloodthorn Cache.
- C-5 Larry's Tackle Box `Wc68sUMJqcjttr2lLtMc-` drops Sea-King's Scale `HSvTtRH06xgCW5XRIcFX2` (index: hidden) at 10%. Rusted Gatherer's Chest has hunter material Mosswolf Tuft first — needs check.
- C-6 Whispering Dawnblade `mqCCZGSfXUNL02B4H6C9R` duplicates Masamune `An9G-YkaAonclWsmcpx4E` description/image/battle text.
- C-7 Visible test/admin items (stale index): Test Item `kuXRVV_fPmInLz5SmzJRa`, Test Armor `fDCSF_o_BZez6-CDFflhf` (consumable), Test Variant `QeQtevFEEL766JJQZ5tWK`, Neo Test `AFybmwGEKISAVFNQift9T`, Ash Test Key `eL5qY9k21c7nfvgQiBaZp`, PVE Test Amor `E6tlRU8OAucemGbYQu55l`, Crimson Dragon Breastplate Test Copy `oUbEs8jhjG98aEKJVmjFh`, Dummy Armor 1–4 (`f5IvuLwZeJjs2I5bV2VjA`, `lHoYU1tYk0bON7ut0_Gcl`, `sLtFbk_CizLUqqcYUULax`, `WAi3_w7BeUcNqnflI3qwz`), SY SY `XhhoU_Y34R1uop8WuUx_U`, N silver reward `gIKW28_N5LQECzDFWXnZY`, Item for Fixing account `4UkvD8_WPviQiRHQvN4xl`, Rep Tech Replacement `uEZzzagRbXcR81Gb9mYrM`. Also: AI Blade 40AP, Genin PVE Damage/Support/Tank, Scroll 4, Scroll 6, Collect Them All, You know what it is. Hiding unequips from all players — check ownership first.
- C-8 Hidden items granted by visible quests (may be intentional quest materials): Subaku Demon Armor `pvSUaWgUeGi7e81tYwxpW` (Subaku Demon Castle `Br7u84Gq7orlEpu0yqy1A`, 15%); Mizu No Odori Sample `iYNVCnkkLg0WAm_oRXdaV` (Marrow Vaults, Stormcourt, Nameless Thorn); Vital plasma samples `Y1GO3wJjnWlXLi6K7ZMeV` (Nameless Thorn, Marrow's Bloodshed).

### Low-quality content
- Offense Crystal 1 `ae5u8QFD2pCYTAtczYuO8`: Arabic numeral, trailing space, description says "stats" but effect is damage given.
- Damage Crystal II `XMsOqatPbFXEEJPtOJ6os` vs Drain Crystal `ipczu2knFPA103pYhzZh3`: same drain, both EPIC, power 100 vs 75 — Drain strictly worse; "Damage II" is really a drain.
- Heal Crystal III `iJM0kb1i6iNXjADJlZGV_`: flat 20 heal on a LEGENDARY; tiers I/II hidden. Needs check (Skyglass Crystal mirrors it, RUL-2026-10-12-005).
- 7 captured crystals have battle description "N/A".
- Chakra Sword `oOdkdJixCLy2bW0Gxo5e0`: effect description `<p>placeholder</p>`, trailing space.
- Night's Testament `osJq3k77YPGoFWgof12FQ`: double spaces in description (rider set accepted by RUL-2026-10-11-004).
- Mastered Shūren no Yaiba `DfV_RZr-4mSvuS1E452aj`: no flavor, broken battle text, 3 damage buckets vs light-rider doctrine (legacy; balance is user's call).
- ~30 effects on 25/44 items say "placeholder" (repo builders write it). Needs check: player visibility.
- Typos: Hemorrhage Cystal `DEILccCULyDDKOz8UqFhM`, Mising Cat, Solider Pill, Celestial Thristle, Dusk's Momento, The Deterrant, Sechi Ruin Alloy, "Dont Die. You're Too Pretty", "KGK Scroll:KX: Hollow Surge", "dEt0uR's Chakra  Sword" (double space), Offense Crystal 1, hidden Calmness Cyrstal.

### Polish
- P-1 Gatherer/Hunter chests share images per tier (5 pairs); all 10 COMMON regardless of tier.
- P-2 slot NONE vs ITEM inconsistent on chests/Serum (Mystery Chest, Common Gatherer's/Hunter's Chest, Serum, hidden vault chests `ixEKlJ0MmDrX7JoMNJVhi`, `6PguSHDJikU8y35qGcBWa`, `h-d58UCSuHN8EZKbLjT5R`).
- P-3 Skyglass Serum `XhilCv1Hq4eNt-Wddok-m`: prevents battle use, PVE-only, only effect 100% heal — maybe unusable. Needs check.
- P-4 Odd type/slot: Lava Sword `pH8rYM-VijrT243G3RhRt` (weapon/KEYSTONE), Old Scroll from the Sand Golem (armor/CHEST), Orb of Shroud (consumable/HAND), Confinement (OTHER/HAND), Snow Crest (accessory/CHEST), Static Hands (accessory/HAND).
- P-5 Near-duplicates: Kaeruun's Ruin Claw vs Ruin Claws; Your Christmas Present vs "… 1"; Shield Crystal vs II both RARE; 7 hidden "X / X +" pairs; hidden "- copy" items.
- P-6 Mixed curly/straight apostrophes.
- P-7 Unicode monospace names: 𝚃𝚠𝚒𝚗𝚋𝚕𝚊𝚍𝚎𝚜 𝚘𝚏 𝚝𝚑𝚎 𝚅𝚎𝚒𝚕, 𝚆𝚑𝚒𝚜𝚙𝚎𝚛𝚎𝚍 𝙴𝚖𝚋𝚎𝚛 (breaks search).
- P-8 Crystal rarity steps inconsistent (Absorb Gem COMMON→EPIC; Heal II/III both LEGENDARY; "Bolster III" lacks "Crystal").
- P-9 49 STATIC assets named "Placeholder" (11 visible, e.g. `KGgk5VvkllsDiqL0zasWQ`); "Ice Field Test 1" `fLrjGRU2tgBHRu2FuBG2K` visible.
- P-10 Asset duplicates: "Shadow field"/"Shadow Field" (`y1hrYiCnjmJM-wK5IIWHa`, `poGzEiz-23-a6BPGrEwnT`), "Chief's Council Chamber" ×2, QuestGiver ×3; trailing spaces "Momo laughing ", "Fiery Dunes Desert ".
- P-11 Default image: Endless Night Chest, AI Heavy Armor (armor in ITEM slot), Ghostly Sovereign's Diadem `LnRVMzyVmVwgaKvTH52Zy` (unreferenced).
- P-12 Indexes stale (Skyglass old names; missing Katana, Reliquary, vault chests, 3 farming items; asset index missing 19 captured + Stormcourt/Ghost Ship scenes). Regenerate via adoption gate.
- P-13 Hidden quests to fix before publish: "Story: The Ember Ledger" `UYlTqs-BzK-9JFmSVnP9l` (29 background fields hold names not ids); "One White Ear" `STAQqoCbpb6I2W39syED_` (6 unknown asset ids).

### Known open from repo
- K-1 Stormrender / push/131 open (B-3).
- K-2 ELEMENTALDAMAGE_DAMAGE_INVESTIGATION_20261020.md: elementaldamage weapons use one preferred element (Fire default), may drop element bonuses. Source-confirmed, not reproduced in game.
- K-3 push/33 open (B-5).
- K-4 Ghost Ship "Still open" 1–3 but quests visible (C-1).
- K-5 bg_wiring_sweep.md / art_backlog.md superseded: Old Ghost `KmGPDnZnGOCvATQqA5LI8` went 45 → 5 objectives between captures 1788136356379 and 1791233210169; all nodes use "Hall Steps Before Dawn" + blank character; 8 approved Forsworn plates + 9 portraits unused in visible quests. Needs check: intentional?
- K-6 active-context says Stormcourt hidden — stale; it is visible.
- K-7 mission_hide_review / push/29 resolved.
- K-8 One Perfect Crop blocked but hidden — no player impact.
- K-9 DRIFT.md is tooling-only.

---

